#!/usr/bin/env python3
"""Generate the "All plugins" catalogue in index.md from the update registry.

Membership is driven by what customers can actually install
(updates.elmspark.com/config.php), not by a hand-typed list. catalogue.json
supplies grouping and editorial copy only.

The build FAILS if a registry plugin is unaccounted for. That is the point:
after this, a newly shipped plugin cannot silently miss the catalogue — it
breaks the build until someone either categorises it or explicitly defers it
in "pending" with a reason.

Usage:
  python3 tools/build-catalogue.py --refresh-registry   # ssh to the VPS first
  python3 tools/build-catalogue.py --check              # validate, write nothing
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "src/content/docs/plugins/index.md"
PAGES = ROOT / "src/content/docs/plugins"
CATALOGUE = ROOT / "catalogue.json"
REGISTRY_CACHE = ROOT / ".registry.json"

PHP = (
    '$r = require "/var/www/updates.elmspark.com/config.php"; '
    '$o = []; foreach ($r as $k => $v) { if (!empty($v["slug"])) '
    '$o[$v["slug"]] = ["tier" => $v["tier"] ?? "foundation", "version" => $v["version"] ?? ""]; } '
    'echo json_encode($o);'
)


def refresh_registry():
    out = subprocess.run(
        ["ssh", "-n", "ionos-ts", f"php -r '{PHP}'"],
        capture_output=True, text=True, check=True,
    ).stdout
    data = json.loads(out)
    REGISTRY_CACHE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"registry refreshed: {len(data)} rows -> {REGISTRY_CACHE.name}")
    return data


def page_title(slug):
    """Title from the doc page frontmatter — the page is the naming authority."""
    p = PAGES / f"{slug}.md"
    if not p.exists():
        return None
    m = re.search(r'^title:\s*"?([^"\n]+)"?\s*$', p.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-registry", action="store_true")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    args = ap.parse_args()

    registry = refresh_registry() if args.refresh_registry else json.loads(
        REGISTRY_CACHE.read_text(encoding="utf-8"))
    cat = json.loads(CATALOGUE.read_text(encoding="utf-8"))

    # EP Suite only. The TIBAI/Discovery products are a separate line.
    ep = {s for s in registry if s.startswith("ep-")}

    listed, dupes = {}, []
    for c in cat["categories"]:
        for e in c["entries"]:
            for s in e["slugs"]:
                if s in listed:
                    dupes.append(s)
                listed[s] = c["name"]

    extra = set(cat.get("extra", {}))
    pending = set(cat.get("pending", {}))

    errors, warnings = [], []

    if dupes:
        errors.append(f"slug listed in more than one category: {', '.join(sorted(set(dupes)))}")

    unaccounted = sorted(ep - set(listed) - pending)
    if unaccounted:
        errors.append(
            "shipped on the channel but not in catalogue.json — categorise it, or add it to "
            f"\"pending\" with a reason: {', '.join(unaccounted)}")

    orphans = sorted(set(listed) - ep - extra)
    if orphans:
        errors.append(
            "listed in catalogue.json but not in the update registry — customers cannot install "
            f"it; move it to \"extra\" or drop it: {', '.join(orphans)}")

    missing_pages = sorted(s for s in set(listed) | extra if not (PAGES / f"{s}.md").exists())
    if missing_pages:
        errors.append(f"listed but has no doc page: {', '.join(missing_pages)}")

    if pending:
        for s in sorted(pending):
            warnings.append(f"PENDING (shipped, undocumented): {s} — {cat['pending'][s]}")

    for w in warnings:
        print(f"  ! {w}", file=sys.stderr)
    if errors:
        print("\nCATALOGUE BUILD FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    # ── Emit ──────────────────────────────────────────────────────────
    lines = ["## All plugins", ""]
    for c in cat["categories"]:
        if not c["entries"]:
            continue
        lines.append(f"### {c['name']}")
        lines.append("")
        rendered = []
        for e in c["entries"]:
            titles = e.get("titles") or [page_title(s) or s for s in e["slugs"]]
            link = " / ".join(
                f"**[{t}](/plugins/{s}/)**" for t, s in zip(titles, e["slugs"]))
            rendered.append((titles[0], f"- {link}. {e['blurb']}"))
        for _sort, line in sorted(rendered, key=lambda r: r[0].lower()):
            lines.append(line)
        lines.append("")
    section = "\n".join(lines).rstrip() + "\n\n"

    text = INDEX.read_text(encoding="utf-8")
    head, rest = text.split("## All plugins", 1)
    tail = "## While you wait" + rest.split("## While you wait", 1)[1]
    new = head + section + tail

    n = sum(len(e["slugs"]) for c in cat["categories"] for e in c["entries"])
    if args.check:
        print(f"check OK — {n} slugs across {len(cat['categories'])} categories"
              f"{' (unchanged)' if new == text else ' (index.md would change)'}")
        return 0

    INDEX.write_text(new, encoding="utf-8")
    print(f"catalogue written: {n} slugs across {len(cat['categories'])} categories")
    print(f"  registry EP rows: {len(ep)} | listed: {len(listed)} | extra: {len(extra)} | pending: {len(pending)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
