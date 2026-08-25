#!/usr/bin/env python3
"""Split the awesome-python README category sections into per-category pages.

Reads site/README.md, moves every `### Category` section under `## Projects`
into its own page at `site/categories/<slug>.md`, and rewrites the Categories
index links to point at those sub-pages.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
SOURCE_README = Path(__file__).resolve().parent.parent / "awesome-python" / "README.md"
README = SITE / "README.md"


def slugify(text: str) -> str:
    """GitHub-style anchor slug (matches the README's existing #anchors)."""
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)  # drop punctuation like & / '
    s = s.replace(" ", "-")
    return s


def main() -> None:
    lines = SOURCE_README.read_text(encoding="utf-8").splitlines()

    projects_idx = next(i for i, l in enumerate(lines) if l.strip() == "## Projects")
    resources_idx = next(i for i, l in enumerate(lines) if l.strip() == "## Resources")

    header = lines[:projects_idx]          # title, sponsors, categories index
    projects = lines[projects_idx + 1 : resources_idx]  # all ### sections
    tail = lines[resources_idx:]           # ## Resources ... end

    # --- split Projects into (group, title, body) sections -----------------
    sections: list[dict] = []
    current_group = None
    current = None
    for line in projects:
        if line.startswith("**") and line.endswith("**") and line.strip() != "**":
            current_group = line.strip().strip("*").strip()
            continue
        if line.startswith("### "):
            if current is not None:
                sections.append(current)
            current = {"group": current_group, "title": line[4:].strip(), "body": []}
            continue
        if current is not None:
            current["body"].append(line)
    if current is not None:
        sections.append(current)

    # --- write each category page ------------------------------------------
    (SITE / "categories").mkdir(exist_ok=True)
    slugs: dict[str, str] = {}
    for sec in sections:
        s = slugify(sec["title"])
        if s in slugs:
            raise SystemExit(f"duplicate slug {s!r}: {slugs[s]} vs {sec['title']}")
        slugs[s] = sec["title"]

    def rewrite_anchor(m: re.Match) -> str:
        target = m.group(1)
        return f"]({target}.md)" if target in slugs else m.group(0)

    for sec in sections:
        title = sec["title"]
        slug = slugify(title)

        body = "\n".join(sec["body"]).strip("\n")
        # cross-category #anchor links now live on their own pages
        body = re.sub(r"\]\(#([^)]+)\)", rewrite_anchor, body)
        page = (
            f"# {title}\n\n"
            f"> Group: **{sec['group']}** · [← All categories](../README.md)\n\n"
            f"{body}\n"
        )
        (SITE / "categories" / f"{slug}.md").write_text(page, encoding="utf-8")

    # --- rewrite the categories index links --------------------------------
    new_header = []
    for line in header:
        new_header.append(re.sub(r"\]\(#([^)]+)\)", r"](categories/\1.md)", line))
    new_readme = "\n".join(new_header).strip("\n") + "\n\n" + "\n".join(tail) + "\n"
    README.write_text(new_readme, encoding="utf-8")

    # --- regenerate sidebar with category navigation -----------------------
    sb = ["- **The List**", "  - [Awesome Python](README.md)", "", "- **Categories**"]
    last_group = None
    for sec in sections:
        if sec["group"] != last_group:
            last_group = sec["group"]
            sb.append(f"  - **{sec['group']}**")
        sb.append(f"    - [{sec['title']}](categories/{slugify(sec['title'])}.md)")
    sb += [
        "",
        "- **Curation**",
        "  - [Curation Context](CONTEXT.md)",
        "  - [Contributing](CONTRIBUTING.md)",
        "  - [Audit Log](docs/audit-logs.md)",
        "  - [ADR: Shortlist, not a catalog](docs/adr/0001-shortlist-not-catalog.md)",
        "",
        "- **Project**",
        "  - [Website Design](DESIGN.md)",
        "  - [Code of Conduct](CODE_OF_CONDUCT.md)",
        "  - [Sponsorship](SPONSORSHIP.md)",
    ]
    (SITE / "_sidebar.md").write_text("\n".join(sb) + "\n", encoding="utf-8")

    print(f"split {len(sections)} categories into {SITE / 'categories'}")
    print("README rewritten (index links -> categories/*.md)")
    print("sidebar regenerated (grouped category navigation)")


if __name__ == "__main__":
    main()
