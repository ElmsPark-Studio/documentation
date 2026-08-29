#!/usr/bin/env python3
"""
PM Field Reports MCP server.

Lets a Claude Code (or any MCP client) session ask the field-reports pool a
question directly, in the same conversation as everything else, rather than
running a script and pasting the output back in. Built because the answer to
"can my agent just read this without a second harness" turned out to be yes,
and MCP is the native way to make that true for a real client rather than a
demo command.

Pure Python 3 standard library. No pip install, no build step, same
discipline as post-report.py, and it reuses that file's signing code rather
than depending on a package. Read-only: this server never publishes an event.
Filing stays in post-report.py, with its human-approval gate; this is purely
for asking questions.

Setup (identical env vars to post-report.py, same key works for both):

    export BUZZ_RELAY_URL=https://relay.example.com
    export BUZZ_PRIVATE_KEY=nsec1...        # or 64-char hex
    export BUZZ_CHANNEL=<channel-uuid>

Then point an MCP client at this file as a stdio server, e.g. in Claude
Code's mcp config:

    {"command": "python3", "args": ["/path/to/field-reports-mcp.py"]}

Tools exposed: list_findings, get_finding, search_findings, pool_health.
"""

import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# BIP-340 Schnorr / bech32 / NIP-98, copied from post-report.py rather than
# imported. Self-contained on purpose: a client fetching this one file should
# get a working server with nothing else to find or install.
# ---------------------------------------------------------------------------
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


def build_event(sk, kind, tags, content):
    pk = pubkey_from_privkey(sk).hex()
    created = int(time.time())
    serial = json.dumps([0, pk, created, kind, tags, content],
                        separators=(",", ":"), ensure_ascii=False)
    eid = hashlib.sha256(serial.encode()).digest()
    return {"id": eid.hex(), "pubkey": pk, "created_at": created, "kind": kind,
            "tags": tags, "content": content, "sig": schnorr_sign(eid, sk).hex()}


USER_AGENT = "pm-field-report-mcp/1.0 (+https://documentation.elmspark.com/guides/pm-field-reports/)"


def nip98_header(sk, url, method):
    tags = [["u", url], ["method", method], ["nonce", os.urandom(8).hex()]]
    ev = build_event(sk, 27235, tags, "")
    token = base64.b64encode(json.dumps(ev, separators=(",", ":")).encode()).decode()
    return "Nostr " + token


def relay_query(relay, sk, filters):
    """POST /query. Read-only: this function is the only network call this
    server ever makes. There is no equivalent write path in this file."""
    url = relay.rstrip("/") + "/query"
    body = json.dumps(filters, separators=(",", ":")).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", nip98_header(sk, url, "POST"))
    req.add_header("User-Agent", USER_AGENT)
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.loads(r.read().decode() or "[]")
    return body if isinstance(body, list) else body.get("events", [])


# ---------------------------------------------------------------------------
# Report parsing + fingerprinting. Mirrors lib/store.php exactly, including
# the 2026-08-23 change dropping pm_core from the hash: a core version is a
# property of a sighting, not of the finding, so it stays a filterable field
# and never enters the fingerprint. Any future change to fr_fingerprint() in
# store.php must be mirrored here, or the two disagree about what counts as
# one finding.
# ---------------------------------------------------------------------------
JSON_BLOCK = re.compile(r"```json\s*(.+?)```", re.S)


def extract_report(content):
    m = JSON_BLOCK.search(content)
    if not m:
        return None
    try:
        payload = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict) or payload.get("spec") != "pm-field-report/1":
        return None
    return payload


def fingerprint(category, title):
    norm = re.sub(r"[^a-z0-9 ]", "", title.lower())
    norm = re.sub(r"\s+", " ", norm.strip())
    return hashlib.sha256((category + "|" + norm).encode()).hexdigest()


def fetch_pool(relay, sk, channel):
    """Every kind-9 event in the channel, parsed into (event, report) pairs
    for the ones that are reports. Ordinary chat is silently skipped, same
    rule the real indexer uses."""
    events = relay_query(relay, sk, [{"kinds": [9], "#h": [channel], "limit": 1000}])
    out = []
    for ev in events:
        r = extract_report(ev.get("content", ""))
        if r:
            out.append((ev, r))
    return out


def group_findings(pool):
    """
    (event, report) pairs -> one row per fingerprint.

    Mirrors fr_finding_state() in lib/store.php. The count is SIGHTINGS ONLY:
    a confirmation re-dates a finding without being a second occurrence, and a
    resolution retires it. Counting rows instead would let a re-confirmation
    inflate the one number triage sorts on, which is the whole reason the three
    events are distinct.
    """
    groups = {}
    for ev, r in pool:
        fp = fingerprint(r.get("category", ""), r.get("title", ""))
        groups.setdefault(fp, []).append((ev, r))

    findings = []
    for fp, entries in groups.items():
        entries.sort(key=lambda pair: pair[0].get("created_at", 0), reverse=True)
        head_ev, head_r = entries[0]

        sightings = [p for p in entries if p[1].get("event", "sighting") == "sighting"]
        confirms  = [p for p in entries if p[1].get("event") == "confirmation"]
        resolves  = [p for p in entries if p[1].get("event") == "resolution"]

        # Most recent evidence the fault is actually present.
        present = sightings + confirms
        present.sort(key=lambda pair: pair[0].get("created_at", 0), reverse=True)
        last_ev, last_r = present[0] if present else (head_ev, head_r)

        status, fixed_in = "open", None
        if resolves:
            res_ev, res_r = resolves[0]
            fixed_in = res_r.get("fixed_in")
            # A confirmation dated after the fix means it came back.
            status = ("reopened"
                      if present and present[0][0].get("created_at", 0) > res_ev.get("created_at", 0)
                      else "resolved")

        findings.append({
            "fingerprint": fp,
            "title": head_r.get("title"),
            "category": head_r.get("category"),
            "severity": head_r.get("severity"),
            "status": status,
            "fixed_in": fixed_in,
            "sightings": len(sightings),
            "confirmations": len(confirms),
            "last_seen_core": last_r.get("pm_core"),
            "last_seen_at": last_ev.get("created_at"),
            "cores_seen": sorted({r.get("pm_core") for _, r in entries if r.get("pm_core")}),
            "reporters": sorted({ev.get("pubkey", "")[:12] for ev, _ in entries}),
            "latest_observed": last_r.get("observed"),
            "latest_event_id": head_ev.get("id"),
        })
    findings.sort(key=lambda f: f["sightings"], reverse=True)
    return findings


# ---------------------------------------------------------------------------
# MCP: newline-delimited JSON-RPC 2.0 over stdio. No SDK: the protocol is
# small enough that implementing it directly keeps this file dependency-free,
# same reasoning as the hand-rolled signer above.
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "list_findings",
        "description": (
            "List findings in the PM field-reports pool, deduplicated and grouped "
            "by sighting. Optionally filter by category, PageMotor core version, "
            "or a free-text search term. This is the 'what is the fleet hitting on "
            "0.11' query."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["bug", "docs-gap", "environment", "idea"]},
                "core": {"type": "string", "description": "PageMotor core version, e.g. 0.11.1"},
                "q": {"type": "string", "description": "Free-text match against title and observed"},
                "status": {"type": "string", "enum": ["open", "resolved", "reopened"],
                            "description": "Only findings in this state. 'open' is what triage wants."},
            },
        },
    },
    {
        "name": "get_finding",
        "description": "Full detail for one finding, including every sighting that grouped onto it.",
        "inputSchema": {
            "type": "object",
            "properties": {"fingerprint": {"type": "string", "description": "Fingerprint, or a leading prefix of it"}},
            "required": ["fingerprint"],
        },
    },
    {
        "name": "search_findings",
        "description": "Free-text search across findings. Use before filing a new report to check for a twin.",
        "inputSchema": {
            "type": "object",
            "properties": {"q": {"type": "string"}},
            "required": ["q"],
        },
    },
    {
        "name": "pool_health",
        "description": "Relay reachability, this identity's pubkey, and a count of findings/reports in the channel.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def env_or_die(name):
    v = os.environ.get(name, "").strip()
    if not v:
        sys.stderr.write("field-reports-mcp: set %s\n" % name)
        sys.exit(1)
    return v


def call_tool(name, args, ctx):
    relay, sk, channel = ctx["relay"], ctx["sk"], ctx["channel"]

    if name == "pool_health":
        t0 = time.time()
        pool = fetch_pool(relay, sk, channel)
        return {
            "relay": relay,
            "pubkey": pubkey_from_privkey(sk).hex(),
            "channel": channel,
            "reports": len(pool),
            "findings": len(group_findings(pool)),
            "open": len([f for f in group_findings(pool) if f["status"] != "resolved"]),
            "query_ms": round((time.time() - t0) * 1000),
        }

    if name in ("list_findings", "search_findings"):
        pool = fetch_pool(relay, sk, channel)
        findings = group_findings(pool)
        if name == "search_findings" or args.get("q"):
            needle = str(args.get("q", "")).lower()
            findings = [f for f in findings
                        if needle in (f["title"] or "").lower()
                        or needle in (f["latest_observed"] or "").lower()]
        if args.get("category"):
            findings = [f for f in findings if f["category"] == args["category"]]
        if args.get("core"):
            findings = [f for f in findings if args["core"] in f["cores_seen"]]
        if args.get("status"):
            findings = [f for f in findings if f["status"] == args["status"]]
        return {"count": len(findings), "findings": findings}

    if name == "get_finding":
        prefix = str(args.get("fingerprint", ""))
        if not prefix:
            raise ValueError("fingerprint is required")
        pool = fetch_pool(relay, sk, channel)
        matches = [(ev, r) for ev, r in pool if fingerprint(r.get("category", ""), r.get("title", "")).startswith(prefix)]
        if not matches:
            return {"found": False}
        matches.sort(key=lambda pair: pair[0].get("created_at", 0))
        return {
            "found": True,
            "fingerprint": fingerprint(matches[0][1].get("category", ""), matches[0][1].get("title", "")),
            "sightings": [
                {
                    "event_id": ev.get("id"),
                    "pubkey": ev.get("pubkey", "")[:16],
                    "created_at": ev.get("created_at"),
                    **r,
                }
                for ev, r in matches
            ],
        }

    raise ValueError("unknown tool: %s" % name)


def rpc_loop(ctx):
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = msg.get("method")
        msg_id = msg.get("id")

        if method == "initialize":
            reply(msg_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "pm-field-reports", "version": "1.0.0"},
            })
        elif method == "notifications/initialized":
            pass  # no response for notifications
        elif method == "tools/list":
            reply(msg_id, {"tools": TOOLS})
        elif method == "tools/call":
            params = msg.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {}) or {}
            try:
                result = call_tool(name, args, ctx)
                reply(msg_id, {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]})
            except Exception as e:  # noqa: BLE001 - report to the client, don't crash the server
                reply(msg_id, {"content": [{"type": "text", "text": "error: %s" % e}], "isError": True})
        elif msg_id is not None:
            reply(msg_id, None, error={"code": -32601, "message": "method not found: %s" % method})


def reply(msg_id, result, error=None):
    if msg_id is None:
        return  # notification, no response expected
    out = {"jsonrpc": "2.0", "id": msg_id}
    out["error" if error else "result"] = error or result
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()


def main():
    ctx = {
        "relay": env_or_die("BUZZ_RELAY_URL"),
        "sk": load_privkey(env_or_die("BUZZ_PRIVATE_KEY")),
        "channel": env_or_die("BUZZ_CHANNEL"),
    }
    rpc_loop(ctx)


if __name__ == "__main__":
    main()
