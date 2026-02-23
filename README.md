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

**Prerequisites:** [Hugo](https://gohugo.io/installation/) (extended not required).

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

- **Papers:** Append or edit entries under `papers:`. Use `selected: true` to show the item in the “Selected Publications” block on the home page. Optional `abbr` is the venue abbreviation in parentheses (e.g. `CCGrid`). Example:

  ```yaml
  - title: "Paper title"
    authors: "P. Jacquet, Co-author"
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

- **Fields:** `title`, `venue`, `year`; optional `location`, `note` (e.g. "Poster"), `links` (list of `label`/`url`).
- Example:

  ```yaml
  talks:
    - title: "Talk title"
      venue: "Event name"
      location: "City or institution"
      year: 2025
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

All service entries (committees, reviews, etc.) live in **`data/service.yaml`**. The display uses a **nested list**: each category (e.g. “Committees”, “Reviews”) is a top-level list item with its own sub-list of items. **On the home page, only the first 5 items per category** (e.g. first 5 committees, first 5 reviews) are shown; the full list is at `/service/`.

- **Structure:** `categories:` is a list of `name` + `items`. Each item has `text` (required); optional `link: { label, url }`; optional `suffix` (e.g. `" Workshop"`); optional **`years`** (list, e.g. `[2025, 2027]`) for multiple years—renders as “ 2025, 2027” after the link/suffix.
- Example (single year via suffix, or multiple years via `years`):

  ```yaml
  categories:
    - name: "Committees"
      items:
        - text: "PC member of Artifact track, "
          link: { label: "DSN", url: "https://..." }
          suffix: " 2026"
        - text: "Web Chair & PC member of "
          link: { label: "INFRASTRUCTURE", url: "https://..." }
          suffix: " Workshop"
          years: [2025, 2027]
    - name: "Reviews"
      items:
        - text: "Journal of Y"
  ```

Then run `hugo --minify`. The home page shows the first 5 items per category; `/service/` shows the full nested list.

### Changing site metadata

- **Site params** (profile image, credit, GitHub/Scholar/LinkedIn): `hugo.yaml` → `params`.
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
| `data/service.yaml` | Single source for service (categories + items) |
| `layouts/index.html` | Home (CV) layout |
| `layouts/blog/list.html`, `single.html` | Blog list and post layout |
| `layouts/publications/list.html` | Publications page layout |
| `layouts/talks/list.html` | Talks page layout |
| `layouts/teaching/list.html` | Teaching page layout |
| `layouts/service/list.html` | Service page layout (same nested list style) |
| `layouts/partials/` | Shared head, sidebars, publication/talk/teaching/service entry |
| `static/resources/` | CSS, JS, favicons (served as `/resources/...`) |
