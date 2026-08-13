# Pierre website

A minimal personal/academic site built with [Hugo](https://gohugo.io/).

- **Home**: CV-style page (intro, selected publications, teaching, talks, service, bio).
- **Blog**: List of articles and individual posts.
- **Publications**: Full list of papers, press, and theses (data-driven from `data/publications.yaml`).
- **Talks**: Full list of talks (data-driven from `data/talks.yaml`); selected talks on home.
- **Teaching**: Full list of courses (data-driven from `data/teaching.yaml`); selected courses on home.
- **Service**: Full list (data-driven from `data/service.yaml`); committees and reviews in nested list style on home and `/service/`.

[Live site](https://jacquetpi.github.io)

---

## Build (compile)

**Prerequisites:** [Hugo](https://gohugo.io/installation/) (extended not required; CI is pinned to v0.165.0).

```bash
hugo --minify
```

Output is in `public/`. To preview locally:

```bash
hugo server
```

Then open http://localhost:1313 .

**GitHub Pages (this repo):** A workflow in [.github/workflows/hugo.yaml](.github/workflows/hugo.yaml) builds and deploys on push to `master`. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. Then the workflow's `public/` artifact is published.

---

## Maintainability

### Adding a blog post (article)

1. Create a new file under `content/blog/` with a `.md` extension, e.g. `content/blog/2025-02-19_my-post.md`.

2. Add front matter and body (Markdown and/or HTML):

   ```yaml
   ---
   title: "My post title"
   date: 2025-02-19
   summary: "Short line shown on the blog list (optional)"
   ---

   Your content here. You can use **Markdown** or raw HTML.
   ```

3. Rebuild with `hugo --minify`. The post will appear on the blog list and at `/articles/<filename-without-ext>.html` (e.g. `/articles/2025-02-19_my-post.html`).

**Dashboard-style post:** To attach the environmental impact dashboard script to a post, name the file `dashboard.md` (or duplicate the conditional in `layouts/blog/single.html` for another filename).

### Adding or editing publications

All publications (papers, press, theses) live in **`data/publications.yaml`**.

- **Papers:** Append or edit entries under `papers:`. Use `selected: true` to show the item in the “Selected Publications” block on the home page. Use full first names in `authors`; the site abbreviates for display (e.g. P. Jacquet) and underlines the site author. Optional `abbr` is the venue abbreviation in parentheses (e.g. `CCGrid`). Optional `keynote: true` adds the same bold + dotted underline title styling as keynote talks (on both home and `/publications/`; non-home pages use `blog.css`). Every entry with a `bib_key` also gets a `[BibTeX]` toggle on the site that shows and copies a plain BibTeX snippet for the publication. Optional `abstract` (plain text) adds an `[Abstract]` toggle right after the first `[Paper]`-labelled link in the links row (before remaining links and `[BibTeX]`). Example:

  ```yaml
  - title: "Paper title"
    authors: "Pierre Jacquet, Co-author"
    venue: "Full venue name"
    abbr: "SHORT"
    year: 2026
    selected: true
    links:
      - label: "[Paper]"
        url: "https://..."
      - label: "[Code]"
        url: "https://..."
  ```

- **Press:** Same idea under `press:` (no `abbr` needed).
- **Theses:** Under `theses:` with `venue` e.g. `"Ph.D. Thesis"` or `"Master Thesis"`.

Then run `hugo --minify` again. The home page and the `/publications/` page both read from this file.

### Adding or editing talks

All talks live in **`data/talks.yaml`**. Use `selected: true` to show a talk in the “Selected Talks” block on the home page.

- **Fields:** `title`, `venue`, `type`, `year`; optional `location`, `month_num` (1-12), `note` (e.g. "Poster"), `links` (list of `label`/`url`), `highlighted` (default `false`). Any number of links is shown as `Title ~ Link1, Link2, …`. If `highlighted: true`, the talk `type` is shown in **bold** with a **dotted underline** on the site and in **bold** in the PDF CV.
- **Order:** Talks are listed by **year** then **month_num** (newest first; unknown month sorts after known months in the same year). Same year/month keeps the order of entries in the file.
- Example:

  ```yaml
  talks:
    - title: "Talk title"
      venue: "Event name"
      location: "City or institution"
      type: "Invited talk"
      highlighted: false
      year: 2025
      month_num: 4
      selected: true
      links:
        - label: "Slides"
          url: "https://..."
  ```

Then run `hugo --minify`. The home page and `/talks/` read from this file.

### Adding or editing teaching (courses)

All courses live in **`data/teaching.yaml`**. Use `selected: true` to show a course in the “Teaching” block on the home page.

- **Fields:** `title`, `institution`, `period` (e.g. "2025/26" or "2022/23, 2023/24"), `selected`.
- Example:

  ```yaml
  courses:
    - title: "Course name"
      institution: "University name"
      period: "2025/26"
      selected: true
  ```

Then run `hugo --minify`. The home page and `/teaching/` read from this file.

### Adding or editing service

All service entries (committees, reviews, etc.) live in **`data/service.yaml`** as a flat `entries:` list. Entries are grouped automatically into display categories by **`domain`** + **`role_group`** (e.g. “Conference - PC Member”, “Journal - Reviewer”, “Organization”), rendered as a nested list. **On the home page, only entries with `selected: true` are shown** (max 5 per resulting category); the full list is at `/service/`.

- **Required fields:** `domain` (`conference` | `journal` | `journal/conference` | `organization`), `role_type` (display label, e.g. "PC Member"), `role_group` (grouping key, e.g. `pc_member`), `venue` (display name).
- **Optional fields:** `url` (venue link), `year` (single year) or `years` (list, renders as "2025, 2027"), `month_num` (1-12, RSS dating), `role_prefix` (text shown before the venue, e.g. "Web Chair"), `note` (rendered in parentheses, e.g. "Workshop"), `sub_reviewing` (informational flag only), `selected` (show on home page). Set **`displayed_on_site: false`** on an entry to show it only in the generated LaTeX CV, not on the website.
- Example:

  ```yaml
  entries:
    - domain: "conference"
      role_type: "PC Member"
      role_group: "pc_member"
      venue: "IEEE/IFIP DSN"
      url: "https://..."
      year: 2026
      month_num: 6
      selected: true
    - domain: "conference"
      role_type: "General Chair"
      role_group: "general_chair"
      role_prefix: "Web Chair"
      venue: "INFRASTRUCTURE"
      url: "https://..."
      note: "Workshop"
      years: [2025, 2027]
  ```

Then run `hugo --minify`. The home page shows selected entries (max 5 per category); `/service/` shows the full nested list.

### LaTeX CV (PDF)

A LaTeX CV is generated from the same data and served at **`/cv/cv.pdf`** (and sources at `/cv/cv.tex`, `/cv/cv.bib`). The generator script **`scripts/generate_cv.py`** reads `data/publications.yaml`, `data/interviews.yaml`, `data/service.yaml`, `data/talks.yaml`, and `data/artifacts.yaml`, then fills the skeleton **`latex/cv_skeleton.tex`** and writes **`latex/cv.bib`** and **`latex/cv.tex`**. CI builds the PDF and copies it (with the generated `.tex` and `.bib`) into `public/cv/` on deploy.

- **To regenerate locally:** `pip install -r scripts/requirements.txt` then `python3 scripts/generate_cv.py`. Build with `cd latex && pdflatex cv.tex && bibtex cv && pdflatex cv.tex && pdflatex cv.tex`. Run tests: `pytest scripts/test_generate_cv.py -v`.
- **Publications:** Use `bib_key`, `entry_type` (`journal` or `conference`), `section_cv` (`main` or `workshop`), and optional `doi`, `pages`, `publisher` (default IEEE) in `data/publications.yaml`; order in the CV follows the file order. Theses use optional `thesis_type` (`phd` or `masters`) for the bib entry type.
- **Service:** `sub_reviewing: true` is an informational flag only (not rendered on the site or in the CV; sub-reviewing entries get their own "Journal - Sub-reviewer" category via `role_group`).
- **Interviews:** `data/interviews.yaml` (each entry: `bib_key`, `title`, `authors`, `year`, optional `note` for URL or text).
- **Artifacts:** `data/artifacts.yaml` (each entry: `name`, `family`, `audience`, `evolution`, `duration`, `contribution`, `url`, `description`).

### RSS feed

`/feed.xml` aggregates **blog posts** (`content/blog/`) and all data-driven entries (publications, talks, teaching, service, interviews, artifacts), sorted newest first. Future-dated entries are excluded until their date has passed, so items appear in readers exactly once (requires git history; CI builds with `fetch-depth: 0`).

### Changing site metadata

- **Site params** (profile image, credit, GitHub/Scholar/LinkedIn): `hugo.yaml` → `params`.
- **Last-updated footer:** the home page shows a "Last updated" date derived from git commit dates (`enableGitInfo: true`).
- **Favicons:** Put favicon files in `static/resources/favicon/` (paths are already referenced in `layouts/partials/head.html`).
- **Styles:** `static/resources/css/cv.css` (home) and `static/resources/css/blog.css` (blog and publications).

### Project layout (reference)

| Path | Role |
|------|------|
| `hugo.yaml` | Base URL, permalinks, params |
| `content/_index.md` | Home page content (intro) |
| `content/blog/*.md` | Blog posts |
| `content/publications/_index.md` | Publications section (body unused; list is data-driven) |
| `content/talks/_index.md` | Talks section (body unused; list is data-driven) |
| `content/teaching/_index.md` | Teaching section (body unused; list is data-driven) |
| `content/service/_index.md` | Service section (body unused; list is data-driven) |
| `data/publications.yaml` | Single source for all publications |
| `data/talks.yaml` | Single source for all talks |
| `data/teaching.yaml` | Single source for all teaching/courses |
| `data/service.yaml` | Single source for service (flat `entries:` list); `displayed_on_site: false` hides entry on site but keeps it in CV |
| `data/interviews.yaml` | Interviews (for CV bib and outreach section) |
| `data/artifacts.yaml` | Research artifacts (for CV “Research artifacts” section) |
| `latex/cv_skeleton.tex` | LaTeX CV template with placeholders; filled by `scripts/generate_cv.py` |
| `scripts/generate_cv.py` | Generates `latex/cv.tex` and `latex/cv.bib` from data/*.yaml |
| `scripts/test_generate_cv.py` | Pytest tests for the CV generator |
| `layouts/index.html` | Home (CV) layout |
| `layouts/404.html` | Custom 404 page (served automatically by GitHub Pages) |
| `layouts/index.feed.xml` | RSS feed template (blog posts + data files) |
| `layouts/blog/list.html`, `single.html` | Blog list and post layout |
| `layouts/publications/list.html` | Publications page layout |
| `layouts/talks/list.html` | Talks page layout |
| `layouts/teaching/list.html` | Teaching page layout |
| `layouts/service/list.html` | Service page layout (same nested list style) |
| `layouts/partials/` | Shared head, sidebars, publication/talk/teaching/service entry |
| `static/resources/` | CSS, JS, favicons (served as `/resources/...`) |
