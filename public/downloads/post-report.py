#!/usr/bin/env python3
"""
Publish a PM field report to a Buzz channel from any platform.

The official `buzz` CLI is a macOS binary, so a Linux or Windows server agent has
no way to post with it. This talks to the relay's HTTP bridge directly instead,
which works anywhere Python 3.8+ runs. Standard library only: no pip install, no
build step, nothing to vendor.

    export BUZZ_RELAY_URL=https://relay.example.com
    export BUZZ_PRIVATE_KEY=<64-char hex, or nsec1...>
    export BUZZ_CHANNEL=<channel uuid>

    cat report.json | ./post-report.py
    ./post-report.py --check          # verify credentials without posting
    ./post-report.py --dry-run < report.json   # print the envelope, send nothing

This script does NOT scrub and does NOT ask permission. Both belong to whatever
assembles the report, and the human approval must happen before this is called.
A published event is signed and effectively permanent.
"""

import base64
import hashlib
import json
import os
import sys
import time
import urllib.request
import urllib.error

# --------------------------------------------------------------------------
# BIP-340 Schnorr signing over secp256k1. Pure Python, no dependencies.
# --------------------------------------------------------------------------
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def _inv(a, n):
    return pow(a, n - 2, n)


def _point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    if p1[0] == p2[0] and p1[1] != p2[1]:
        return None
    if p1 == p2:
        lam = (3 * p1[0] * p1[0] * _inv(2 * p1[1], P)) % P
    else:
        lam = ((p2[1] - p1[1]) * _inv(p2[0] - p1[0], P)) % P
    x3 = (lam * lam - p1[0] - p2[0]) % P
    return (x3, (lam * (p1[0] - x3) - p1[1]) % P)


def _point_mul(p, n):
    r = None
    for i in range(256):
        if (n >> i) & 1:
            r = _point_add(r, p)
        p = _point_add(p, p)
    return r


def _tagged_hash(tag, msg):
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + msg).digest()


def _has_even_y(p):
    return p[1] % 2 == 0


def pubkey_from_privkey(sk_bytes):
    d = int.from_bytes(sk_bytes, "big")
    if not (1 <= d <= N - 1):
        raise ValueError("private key out of range")
    return _point_mul(G, d)[0].to_bytes(32, "big")


def schnorr_sign(msg32, sk_bytes):
    d0 = int.from_bytes(sk_bytes, "big")
    if not (1 <= d0 <= N - 1):
        raise ValueError("private key out of range")
    point = _point_mul(G, d0)
    d = d0 if _has_even_y(point) else N - d0
    px = point[0].to_bytes(32, "big")

    aux = os.urandom(32)
    t = (d ^ int.from_bytes(_tagged_hash("BIP0340/aux", aux), "big")).to_bytes(32, "big")
    k0 = int.from_bytes(_tagged_hash("BIP0340/nonce", t + px + msg32), "big") % N
    if k0 == 0:
        raise RuntimeError("nonce generation failed, retry")

    r_point = _point_mul(G, k0)
    k = k0 if _has_even_y(r_point) else N - k0
    rx = r_point[0].to_bytes(32, "big")

    e = int.from_bytes(_tagged_hash("BIP0340/challenge", rx + px + msg32), "big") % N
    return rx + ((k + e * d) % N).to_bytes(32, "big")


# --------------------------------------------------------------------------
# bech32 (NIP-19) decoding, so an nsec1 key works as well as raw hex
# --------------------------------------------------------------------------
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


_BECH32_GEN = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]


def _bech32_polymod(values):
    chk = 1
    for v in values:
        top = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ v
        for i in range(5):
            chk ^= _BECH32_GEN[i] if ((top >> i) & 1) else 0
    return chk


def _hrp_expand(hrp):
    return [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]


def _bech32_decode(s, expected_hrp):
    """
    Decode a bech32 string, verifying BOTH the checksum and the human-readable
    prefix.

    Both checks matter more than they look. A mistyped key does not decode to
    something invalid: it decodes to a different, perfectly valid 32-byte
    scalar, which then signs perfectly valid events as an identity that is not
    a member of anything. The relay rejects it as unauthorised, so the error
    points at membership while the real fault is a typo. The checksum exists
    to catch exactly that, six characters earlier and with a useful message.

    The prefix check is belt and braces: the caller already screens for an
    nsec1 prefix, but a decoder that silently accepts any prefix is one
    refactor away from letting a public key be used as a private one.
    """
    s = s.strip().lower()
    pos = s.rfind("1")
    if pos < 1:
        raise ValueError("not a bech32 string")

    hrp = s[:pos]
    if hrp != expected_hrp:
        raise ValueError("expected a %s key, got %s" % (expected_hrp, hrp))

    data = [CHARSET.find(c) for c in s[pos + 1:]]
    if any(d == -1 for d in data):
        raise ValueError("bad bech32 character")
    if len(data) < 6:
        raise ValueError("bech32 string too short")
    if _bech32_polymod(_hrp_expand(hrp) + data) != 1:
        raise ValueError("checksum failed, the key is mistyped")

    acc = bits = 0
    out = bytearray()
    for value in data[:-6]:
        acc = (acc << 5) | value
        bits += 5
        while bits >= 8:
            bits -= 8
            out.append((acc >> bits) & 0xFF)
    return bytes(out)


def load_privkey(raw):
    raw = raw.strip()
    if raw.lower().startswith("npub1"):
        raise SystemExit("that is a PUBLIC key. BUZZ_PRIVATE_KEY needs the nsec1 half")
    if raw.lower().startswith("nsec1"):
        try:
            key = _bech32_decode(raw, "nsec")
        except ValueError as e:
            raise SystemExit("BUZZ_PRIVATE_KEY: %s" % e)
    else:
        try:
            key = bytes.fromhex(raw)
        except ValueError:
            raise SystemExit("BUZZ_PRIVATE_KEY is neither 64-char hex nor an nsec1 string")
    if len(key) != 32:
        raise SystemExit("private key must be 32 bytes")
    return key


# --------------------------------------------------------------------------
# Nostr events
# --------------------------------------------------------------------------
def build_event(sk, kind, tags, content):
    pk = pubkey_from_privkey(sk).hex()
    created = int(time.time())
    serial = json.dumps([0, pk, created, kind, tags, content],
                        separators=(",", ":"), ensure_ascii=False)
    eid = hashlib.sha256(serial.encode()).digest()
    return {
        "id": eid.hex(),
        "pubkey": pk,
        "created_at": created,
        "kind": kind,
        "tags": tags,
        "content": content,
        "sig": schnorr_sign(eid, sk).hex(),
    }


def nip98_header(sk, url, method):
    """
    NIP-98: a signed kind-27235 event proves who is making this HTTP call.

    The nonce matters. created_at has one-second resolution, so two calls in the
    same second would produce byte-identical auth events with the same id, and
    the relay rejects the second as a replay. A random tag keeps each one unique.
    """
    tags = [["u", url], ["method", method], ["nonce", os.urandom(8).hex()]]
    ev = build_event(sk, 27235, tags, "")
    token = base64.b64encode(json.dumps(ev, separators=(",", ":")).encode()).decode()
    return "Nostr " + token


def post(relay, path, sk, payload):
    url = relay.rstrip("/") + path
    body = json.dumps(payload, separators=(",", ":")).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", nip98_header(sk, url, "POST"))
    # Identify ourselves properly. urllib's default agent string trips bot
    # protection on some CDNs, which surfaces as an opaque 403 that looks like
    # an authentication failure but never reaches the relay at all.
    req.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}


# --------------------------------------------------------------------------
# Report envelope
# --------------------------------------------------------------------------
USER_AGENT = "pm-field-report-client/1.0 (+https://documentation.elmspark.com/guides/pm-field-reports/)"

REQUIRED = ["spec", "category", "severity", "title", "pm_core", "observed"]
CATEGORIES = ("bug", "docs-gap", "environment", "idea")
SEVERITIES = ("blocker", "major", "minor", "note")


def build_envelope(report):
    missing = [k for k in REQUIRED if not str(report.get(k, "")).strip()]
    if missing:
        raise SystemExit("missing required field(s): " + ", ".join(missing))
    if report["spec"] != "pm-field-report/1":
        raise SystemExit("spec must be pm-field-report/1")
    if report["category"] not in CATEGORIES:
        raise SystemExit("bad category: " + str(report["category"]))
    if report["severity"] not in SEVERITIES:
        raise SystemExit("bad severity: " + str(report["severity"]))

    # A bug with no reproduction steps is a hunch, and hunches are what silt a
    # shared pool up. The guide has always said so; the client now enforces it.
    repro = report.get("repro")
    if report["category"] == "bug":
        if not isinstance(repro, list) or not [s for s in repro if str(s).strip()]:
            raise SystemExit("category 'bug' needs repro: a non-empty array of steps")
    if repro is not None and not isinstance(repro, list):
        raise SystemExit("repro must be an array of steps")

    bits = ["PM " + str(report["pm_core"])]
    if report.get("php"):
        bits.append("PHP " + str(report["php"]))
    if report.get("environment"):
        bits.append(str(report["environment"]))

    head = "**[{} / {}]** {}".format(report["category"], report["severity"], report["title"])
    body = json.dumps(report, indent=2, ensure_ascii=False)
    return "{}\n\n{}\n\n```json\n{}\n```".format(head, " · ".join(bits), body)


def main():
    relay = os.environ.get("BUZZ_RELAY_URL", "").strip()
    channel = os.environ.get("BUZZ_CHANNEL", "").strip()
    keyraw = os.environ.get("BUZZ_PRIVATE_KEY", "").strip()

    for name, val in (("BUZZ_RELAY_URL", relay), ("BUZZ_PRIVATE_KEY", keyraw)):
        if not val:
            raise SystemExit("set " + name)

    sk = load_privkey(keyraw)

    if "--check" in sys.argv:
        print("relay:  " + relay)
        print("pubkey: " + pubkey_from_privkey(sk).hex())
        status, body = post(relay, "/query", sk, [{"kinds": [9], "limit": 1}])
        print("query:  HTTP {} {}".format(status, "ok" if status == 200 else body))
        return

    # Reading the channel is part of the filing discipline, not an extra. Two
    # steps need it: checking for an existing twin BEFORE filing, so a sighting
    # groups instead of silently splitting the finding, and confirming what came
    # back afterwards. Reads only, never /events.
    if "--search" in sys.argv:
        if not channel:
            raise SystemExit("set BUZZ_CHANNEL")
        terms = [a for a in sys.argv[1:] if not a.startswith("-")]
        needle = " ".join(terms).lower()
        status, body = post(relay, "/query", sk,
                            [{"kinds": [9], "#h": [channel], "limit": 200}])
        if status != 200:
            raise SystemExit("relay refused the read: HTTP {} {}".format(status, body))

        events = body if isinstance(body, list) else body.get("events", [])
        hits = 0
        for ev in events:
            content = ev.get("content", "")
            head = content.split("\n", 1)[0].strip()
            if needle and needle not in content.lower():
                continue
            hits += 1
            print("{}  {}".format(ev.get("id", "")[:10], head[:100]))
        print("\n{} of {} message(s){}".format(
            hits, len(events), " matching " + repr(needle) if needle else ""))
        print("Reuse an existing title VERBATIM if one of these is your finding, "
              "or it files as a separate one.")
        return

    if not channel:
        raise SystemExit("set BUZZ_CHANNEL")

    raw = sys.stdin.read()
    try:
        report = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit("stdin is not valid JSON: " + str(e))

    content = build_envelope(report)

    if "--dry-run" in sys.argv:
        print(content)
        return

    event = build_event(sk, 9, [["h", channel]], content)
    # The bridge takes the signed event bare at the top level, not wrapped.
    status, body = post(relay, "/events", sk, event)
    if status == 200 and body.get("accepted"):
        print("published " + event["id"])
    else:
        raise SystemExit("relay refused it: HTTP {} {}".format(status, body))


if __name__ == "__main__":
    main()
