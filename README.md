# Awesome Python — Docsify Site

Static website generated from the [`vinta/awesome-python`](https://github.com/vinta/awesome-python) GitHub repository, following `SKILL.md`.

## Structure

```
site/
├── index.html           # Docsify entry point (loads markdown client-side)
├── _sidebar.md          # Navigation sidebar
├── README.md            # The Awesome Python list (homepage)
├── CONTEXT.md           # Curation context
├── CONTRIBUTING.md      # Contributing guide
├── CODE_OF_CONDUCT.md   # Contributor covenant
├── SPONSORSHIP.md       # Sponsorship page
├── DESIGN.md            # Website design notes
├── docs/
│   ├── audit-logs.md
│   └── adr/0001-shortlist-not-catalog.md
└── .nojekyll
```

## Run locally

Docsify renders client-side, so it must be served over HTTP (not `file://`):

```bash
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

Or with any static server:

```bash
npx serve site
```
