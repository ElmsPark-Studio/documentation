#!/usr/bin/env python3
"""Generate the "All plugins" catalogue in index.md from the update registry.

Membership is driven by what customers can actually install
(updates.elmspark.com/config.php), not by a hand-typed list. catalogue.json
supplies grouping and editorial copy only.

The build FAILS if a registry plugin is unaccounted for. That is the point:
after this, a newly shipped plugin cannot silently miss the catalogue — it
breaks the build until someone either categorises it or explicitly defers it
in "pending" with a reason.

It also FAILS if a doc page has fallen behind the version the channel serves.
The registry announces these pages as each plugin's *changelog* URL, so a page
that does not name the shipped version is a broken promise to the customer who
clicked "what changed?" in the Updates screen. A page is current when the
newest "### <version>" heading in its "## Changelog" section equals the
registry version. Pages that have not been brought up to that standard yet are
listed in catalogue.json "changelog_backlog" (slug -> the version the page
documents today, or "none"); those warn instead of failing, and the build tells
you the moment one of them becomes current so the list stays honest.

Usage:
  python3 tools/build-catalogue.py --refresh-registry   # ssh to the VPS first
  python3 tools/build-catalogue.py --check              # validate, write nothing
  python3 tools/build-catalogue.py --seed-changelog-backlog
                                   # record every currently-behind page in
                                   # catalogue.json, so the gate starts green
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


def documented_version(slug):
    """Newest version the doc page's own changelog names, or None if it has no
    changelog section at all. The page is the changelog URL the registry
    announces, so this is what a customer clicking "what changed?" is shown."""
    p = PAGES / f"{slug}.md"
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    if "## Changelog" not in text:
        return None
    section = re.split(r"^## ", text.split("## Changelog", 1)[1], flags=re.M)[0]
    heads = re.findall(r"^###\s+v?([0-9][0-9.a-z-]*)\s*$", section, re.M)
    return heads[0] if heads else None


def check_versions(slugs, registry, backlog):
    """Compare each doc page's newest changelog entry with the shipped version.

    Returns (errors, warnings, current_count, behind). Slugs in the backlog warn
    rather than fail — except when they have caught up, which is an error asking
    for the entry to be removed, so the list can never quietly outlive its
    reason. `behind` is the known-stale roll-up, summarised in one line by
    default so 88 warnings never drown the four that need acting on.
    """
    errors, warnings, current, behind = [], [], 0, []

    for slug in sorted(slugs):
        channel = (registry.get(slug) or {}).get("version", "")
        if not channel:
            continue
        documented = documented_version(slug)
        shows = documented or "none"

        if slug not in backlog:
            if documented is None:
                errors.append(
                    f"{slug}: no \"## Changelog\" section, but the registry announces this page "
                    f"as its changelog URL (channel serves {channel}). Add the section, or add "
                    f"the slug to \"changelog_backlog\" in catalogue.json")
            elif documented != channel:
                errors.append(
                    f"{slug}: page documents {documented}, channel serves {channel} — a customer "
                    f"clicking \"what changed?\" for {channel} is reading {documented}")
            else:
                current += 1
            continue

        if documented == channel:
            errors.append(
                f"{slug}: page is now current at {channel} — remove it from "
                f"\"changelog_backlog\" in catalogue.json")
        elif backlog[slug] != shows:
            warnings.append(
                f"CHANGELOG BACKLOG (moved): {slug} — recorded as \"{backlog[slug]}\", page now "
                f"documents \"{shows}\", channel serves {channel}; update the recorded value")
        else:
            behind.append(f"{slug} — page documents {shows}, channel serves {channel}")

    stale = sorted(set(backlog) - set(slugs))
    if stale:
        errors.append(
            "in \"changelog_backlog\" but no longer a catalogued plugin with a page — drop the "
            f"entry: {', '.join(stale)}")

    return errors, warnings, current, behind


def seed_changelog_backlog(cat, slugs, registry):
    """Record every page that is behind its shipped version, so the gate starts
    green and the backlog doubles as the work queue. Existing entries are kept."""
    backlog = dict(cat.get("changelog_backlog", {}))
    added = 0
    for slug in sorted(slugs):
        channel = (registry.get(slug) or {}).get("version", "")
        if not channel or slug in backlog:
            continue
        documented = documented_version(slug)
        if documented != channel:
            backlog[slug] = documented or "none"
            added += 1
    cat["changelog_backlog"] = dict(sorted(backlog.items()))
    CATALOGUE.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"changelog_backlog seeded: {added} added, {len(backlog)} total -> {CATALOGUE.name}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-registry", action="store_true")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--seed-changelog-backlog", action="store_true",
                    help="record every currently-behind page in catalogue.json and exit")
    ap.add_argument("--backlog", action="store_true",
                    help="list every backlogged page instead of the one-line summary")
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
    backlog = cat.get("changelog_backlog", {})

    if args.seed_changelog_backlog:
        return seed_changelog_backlog(
            cat, [s for s in listed if s in ep and (PAGES / f"{s}.md").exists()], registry)

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

    # Version currency: the page must name the version the channel serves.
    # Only pages that exist and are catalogued are gated; missing pages are
    # already an error above, and "pending" plugins have no page by definition.
    version_errors, version_warnings, current, behind = check_versions(
        [s for s in listed if s in ep and (PAGES / f"{s}.md").exists()], registry, backlog)
    errors += version_errors
    warnings += version_warnings
    if behind:
        if args.backlog:
            warnings += [f"CHANGELOG BACKLOG: {b}" for b in behind]
        else:
            warnings.append(
                f"CHANGELOG BACKLOG: {len(behind)} pages behind the version the channel serves "
                f"(run --backlog to list them)")

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
    currency = f"changelog currency: {current} current, {len(backlog)} in backlog"
    if args.check:
        print(f"check OK — {n} slugs across {len(cat['categories'])} categories"
              f"{' (unchanged)' if new == text else ' (index.md would change)'}")
        print(f"  {currency}")
        return 0

    INDEX.write_text(new, encoding="utf-8")
    print(f"catalogue written: {n} slugs across {len(cat['categories'])} categories")
    print(f"  registry EP rows: {len(ep)} | listed: {len(listed)} | extra: {len(extra)} | pending: {len(pending)}")
    print(f"  {currency}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
