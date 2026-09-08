#!/usr/bin/env python3
"""Scaffold a doc page's Changelog section from the plugin's own CHANGELOG.md.

The update registry announces documentation.elmspark.com/plugins/<slug>/ as each
plugin's *changelog* URL, so a page that does not name the shipped version is a
broken promise to the customer who clicked "what changed?" in their Updates
screen. build-catalogue.py enforces that. Closing each gap by hand is the reason
81 pages sat in the backlog, because the facts already exist in the plugin's own
CHANGELOG.md and were being retyped.

This tool copies the missing entries across in the exact shape the gate expects.
It deliberately does NOT publish them. CHANGELOG.md is written for a developer:
it names PHP flags, core file paths, test rigs and the person who reported the
bug. A customer reading the Updates screen should see none of that. So every
entry is inserted carrying a DRAFT marker, build-catalogue.py fails while any
marker survives, and the marker only goes away when a human has rewritten the
entry and deleted the line. Scaffold, then edit; never scaffold and ship.

Two escape hatches for the authoring side:
  * Wrap developer-only prose in <!-- internal --> ... <!-- /internal --> inside
    CHANGELOG.md and it is stripped on the way across.
  * The report flags entries that smell internal (file paths, PHP fragments, rig
    names, "reported by") so a reviewer knows which ones actually need work.

Usage:
  python3 tools/scaffold-changelog.py                  # report, write nothing
  python3 tools/scaffold-changelog.py --slug ep-blog   # one plugin
  python3 tools/scaffold-changelog.py --write          # apply
  python3 tools/scaffold-changelog.py --list-drafts    # pages awaiting review
"""
import argparse
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "src/content/docs/plugins"
REGISTRY_CACHE = ROOT / ".registry.json"
DEFAULT_PLUGINS = pathlib.Path(
    os.environ.get("EP_PLUGINS_DIR", "~/Developer/elmspark/plugins")).expanduser()

# build-catalogue.py greps for this substring; keep the two in step.
DRAFT_TOKEN = "unreviewed: scaffolded"
DRAFT_MARKER = (
    f"<!-- {DRAFT_TOKEN} from the plugin CHANGELOG.md. Rewrite for a customer, "
    "then delete this line. -->")

# Heuristics: prose that reads like it was written for us, not for a customer.
SMELLS = [
    (re.compile(r"\b(?:lib|src|includes)/[\w./-]+\.(?:php|md|js)"), "core/source file path"),
    (re.compile(r"=>\s*(?:true|false)|\$\w+\b|::\w+\(|\bclass_exists\("), "PHP fragment"),
    (re.compile(r"\brigs?\b|dev11b|\.elmspark\.com|localhost", re.I), "rig or internal host"),
    (re.compile(r"\b(?:reported|found|traced|proven|caught)\b[^.]{0,40}\bby\b", re.I), "attribution or process note"),
    (re.compile(r"\bon the (?:PM|PageMotor) forum\b|@\w+", re.I), "forum handle"),
    (re.compile(r"\b\d{4}-\d{2}-\d{2}\b"), "raw ISO date"),
    # Inline code in a changelog entry is almost always an internal identifier
    # (a header name, a method, a private property) rather than something a
    # customer types. Cheap, and it is the signal the other patterns miss.
    (re.compile(r"`[^`\n]+`"), "inline code identifiers"),
    (re.compile(r"\b(?:PM|PageMotor) \d|\b(?:PageMotor|PM) core\b|\bcore (?:bug|regression|behaviour)\b", re.I),
     "core-internals framing"),
]


def vkey(v):
    """Sortable key. 1.10.48 must outrank 1.9.0, so compare numerically, and
    keep any trailing letter (0.11.2b) as a tiebreak below the plain release."""
    parts = re.findall(r"\d+|[a-z]+", v or "")
    out = []
    for p in parts:
        out.append((0, int(p)) if p.isdigit() else (1, p))
    return out


def load_registry():
    if not REGISTRY_CACHE.exists():
        sys.exit("no .registry.json — run: python3 tools/build-catalogue.py --refresh-registry")
    return json.loads(REGISTRY_CACHE.read_text(encoding="utf-8"))


def strip_internal(body):
    return re.sub(r"<!--\s*internal\s*-->.*?<!--\s*/internal\s*-->", "",
                  body, flags=re.S | re.I).strip()


def parse_plugin_changelog(path):
    """[(version, date, body)] newest first, as the file lists them."""
    text = path.read_text(encoding="utf-8")
    hits = list(re.finditer(r"^##\s+v?([0-9][0-9a-z.]*)\s*[—-]\s*(\S+)\s*$", text, re.M))
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        out.append((m.group(1), m.group(2), strip_internal(text[m.end():end])))
    return out


def page_changelog_versions(page_text):
    if "## Changelog" not in page_text:
        return None
    section = re.split(r"^## ", page_text.split("## Changelog", 1)[1], flags=re.M)[0]
    return re.findall(r"^###\s+v?([0-9][0-9.a-z-]*)\s*$", section, re.M)


def review_flags(body):
    return sorted({label for rx, label in SMELLS if rx.search(body)})


def render(version, body):
    return f"### {version}\n\n{DRAFT_MARKER}\n\n{body.strip()}\n"


def plan_for(slug, registry, plugins_dir, backfill=False):
    """(status, versions_to_insert, notes). status drives the report only."""
    page = PAGES / f"{slug}.md"
    if not page.exists():
        return "no-page", [], "no doc page exists; write the page first"
    chlog = plugins_dir / slug / "CHANGELOG.md"
    if not chlog.exists():
        return "no-changelog", [], f"no CHANGELOG.md at {chlog}"

    channel = (registry.get(slug) or {}).get("version", "")
    if not channel:
        return "not-shipped", [], "not on the update channel"

    text = page.read_text(encoding="utf-8")
    if DRAFT_TOKEN in text:
        return "draft-pending", [], "already holds an unreviewed draft; review it before scaffolding more"

    documented = page_changelog_versions(text)
    have = set(documented or [])
    entries = parse_plugin_changelog(chlog)
    if not entries:
        return "unparsed", [], "CHANGELOG.md has no '## <version>' headings"

    # Never document a version the channel does not serve.
    ceiling = vkey(channel)
    candidates = [e for e in entries if e[0] not in have and vkey(e[0]) <= ceiling]

    if backfill:
        missing = candidates
    elif documented:
        # The gate only cares that the NEWEST documented version matches what
        # ships. Close that gap and nothing else: handing a reviewer eleven
        # historical entries to satisfy a one-version shortfall is how a backlog
        # stops getting worked. --backfill opts into the full history.
        floor = vkey(documented[0])
        missing = [e for e in candidates if vkey(e[0]) > floor]
    else:
        # No changelog section at all: seed it with the shipped version.
        missing = [e for e in candidates if vkey(e[0]) == ceiling][:1] or candidates[:1]

    if not missing:
        return ("current" if documented and vkey(documented[0]) >= ceiling
                else "nothing-to-add"), [], ""
    return "scaffold", missing, ""


def apply(slug, missing):
    """Insert newest-first at the top of the Changelog section, creating the
    section when the page has none. Idempotent: a page holding a draft marker is
    refused upstream, and versions already present are filtered out."""
    page = PAGES / f"{slug}.md"
    text = page.read_text(encoding="utf-8")
    block = "\n".join(render(v, b) for v, _d, b in
                      sorted(missing, key=lambda e: vkey(e[0]), reverse=True))
    if "## Changelog" in text:
        head, rest = text.split("## Changelog", 1)
        new = head + "## Changelog\n\n" + block + rest.lstrip("\n")
    else:
        new = text.rstrip("\n") + "\n\n## Changelog\n\n" + block
    page.write_text(new, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="one plugin slug (default: every shipped slug)")
    ap.add_argument("--write", action="store_true", help="apply; default reports only")
    ap.add_argument("--limit", type=int, help="stop after N pages, for working the backlog down")
    ap.add_argument("--list-drafts", action="store_true", help="pages holding an unreviewed draft")
    ap.add_argument("--backfill", action="store_true",
                    help="also add older entries the page never had, not just the gap to the shipped version")
    ap.add_argument("--plugins-dir", type=pathlib.Path, default=DEFAULT_PLUGINS)
    args = ap.parse_args()

    if args.list_drafts:
        held = [p.stem for p in sorted(PAGES.glob("*.md"))
                if DRAFT_TOKEN in p.read_text(encoding="utf-8")]
        for s in held:
            print(f"  draft awaiting review: {s}")
        print(f"{len(held)} page(s) awaiting review")
        return 1 if held else 0

    registry = load_registry()
    slugs = [args.slug] if args.slug else sorted(registry)

    todo, skipped, done = [], {}, 0
    for slug in slugs:
        status, missing, note = plan_for(slug, registry, args.plugins_dir, args.backfill)
        if status == "scaffold":
            todo.append((slug, missing))
        elif status == "current":
            done += 1
        else:
            skipped.setdefault(status, []).append(f"{slug}{': ' + note if note else ''}")

    if args.limit:
        todo = todo[:args.limit]

    for slug, missing in todo:
        vers = ", ".join(v for v, _, _ in missing)
        print(f"\n{slug}: {len(missing)} entry(s) to add — {vers}")
        for v, _d, body in missing:
            flags = review_flags(body)
            sev = "heavy" if len(flags) >= 3 else "some" if flags else "light"
            print(f"    {v}: [{sev}] {'; '.join(flags) if flags else 'no internal markers found'}")
        if args.write:
            apply(slug, missing)
            print("    written, marked unreviewed")

    print()
    for status, items in sorted(skipped.items()):
        print(f"{status}: {len(items)}")
        if status in ("draft-pending", "no-changelog", "unparsed"):
            for i in items[:10]:
                print(f"    {i}")
    print(f"already current: {done}")
    print(f"pages needing entries: {len(todo)}")
    if args.write and todo:
        print("\nEvery inserted entry carries a DRAFT marker and build-catalogue.py")
        print("will FAIL until each one is rewritten for a customer and the marker")
        print("deleted. Review with: python3 tools/scaffold-changelog.py --list-drafts")
    elif todo:
        print("\nreport only — pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
