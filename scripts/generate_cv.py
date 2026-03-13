#!/usr/bin/env python3
"""
Generate cv/cv.bib and cv/cv.tex from data/*.yaml.
Run from repository root.
"""
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
CV_DIR = REPO_ROOT / "latex"
SKELETON_PATH = CV_DIR / "cv_skeleton.tex"
OUT_TEX_PATH = CV_DIR / "cv.tex"
OUT_BIB_PATH = CV_DIR / "cv.bib"


def load_yaml(name):
    path = DATA_DIR / f"{name}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def latex_escape(s):
    """Minimal LaTeX escaping. Does not escape braces so accent macros like {\\'e} stay valid."""
    if not s:
        return s
    s = s.replace("&", "\\&")
    s = s.replace("%", "\\%")
    s = s.replace("#", "\\#")
    s = s.replace("_", "\\_")
    # Common accents (produce {\'e} etc.; do not escape { } so these remain valid)
    s = s.replace("é", "{\\'e}")
    s = s.replace("è", "{\\`e}")
    s = s.replace("ê", "{\\^e}")
    s = s.replace("à", "{\\`a}")
    s = s.replace("ô", "{\\^o}")
    s = s.replace("ç", "{\\c c}")
    s = s.replace("ï", "{\\\"i}")
    s = s.replace("ë", "{\\\"e}")
    s = s.replace("ù", "{\\`u}")
    s = s.replace("î", "{\\^i}")
    s = s.replace("É", "{\\'E}")
    s = s.replace("È", "{\\`E}")
    s = s.replace("à", "{\\`a}")
    return s


def bib_author(authors_str, bold_me=True):
    """Convert 'Pierre Jacquet, Camille Coti, ...' to LaTeX with bold for Pierre Jacquet (any position)."""
    if not authors_str:
        return ""
    parts = [p.strip().lstrip("and ").strip() for p in re.split(r",\s*|\s+and\s+", authors_str)]
    parts = [p for p in parts if p]
    out = []
    for part in parts:
        if bold_me and ("P. Jacquet" in part or ("Jacquet" in part and "Pierre" in part)):
            out.append("\\textbf{Jacquet}, \\textbf{Pierre}")
        else:
            out.append(part)
    return " and ".join(out)


def format_venue_red(venue, abbr):
    """Format venue with red acronym for bib."""
    if not abbr:
        return latex_escape(venue)
    return f"{latex_escape(venue)} ({{\\textcolor{{red}}{{\\textit{{{abbr}}}}}}})"


def get_first_link_url(links, label_contains=None):
    if not links:
        return None
    for link in links:
        if label_contains is None or (label_contains and label_contains.lower() in link.get("label", "").lower()):
            return link.get("url")
    return links[0].get("url") if links else None


def latex_escape_url(url):
    """Escape URL for use in LaTeX \\href{}{} or \\url{} (e.g. % and #)."""
    if not url:
        return url
    return url.replace("%", "\\%").replace("#", "\\#")


def generate_bib():
    pub = load_yaml("publications")
    interviews = load_yaml("interviews")
    bib_entries = []

    # Papers: journal -> @article, conference -> @inproceedings
    for p in pub.get("papers", []):
        key = p["bib_key"]
        entry_type = p.get("entry_type", "conference")
        bib_type = "article" if entry_type == "journal" else "inproceedings"
        author = bib_author(p.get("authors", ""))
        title = "{{" + latex_escape(p["title"]) + "}}"
        venue_fmt = format_venue_red(p["venue"], p.get("abbr", ""))
        year = p["year"]

        lines = [f"@{bib_type}{{{key},", f"  TITLE = {title},", f"  AUTHOR = {{{author}}},"]
        if bib_type == "article":
            lines.append(f"  JOURNAL = {{{venue_fmt}}},")
        else:
            lines.append(f"  BOOKTITLE = {{{venue_fmt}}},")
        if "EuroSys" in p.get("venue", "") or "European Conference" in p.get("venue", ""):
            lines.append("  PUBLISHER = {{ACM}},")
        else:
            lines.append("  PUBLISHER = {{IEEE}},")
        lines.append(f"  year={{{year}}},")
        if p.get("pages"):
            lines.append(f"  pages={{{p['pages']}}},")
        if p.get("doi"):
            lines.append(f"  DOI = {{{p['doi']}}},")
        url = get_first_link_url(p.get("links"))
        if url:
            lines.append(f"  URL = {{{latex_escape_url(url)}}},")
        lines.append("}")
        bib_entries.append("\n".join(lines))

    # Press
    for p in pub.get("press", []):
        key = p["bib_key"]
        author = bib_author(p.get("authors", ""))
        title = "{{" + latex_escape(p["title"]) + "}}"
        journal = p.get("journal") or p.get("venue", "")
        year = p["year"]
        note_parts = []
        if p.get("note") and not p.get("note", "").startswith("http"):
            note_parts.append(latex_escape(p["note"]))
        url = get_first_link_url(p.get("links"))
        if not url and p.get("note", "").startswith("http"):
            url = p["note"]
        if url:
            note_parts.append(f"\\newline\\url{{{latex_escape_url(url)}}}")
        note = " ".join(note_parts) if note_parts else ""
        lines = [f"@article{{{key},", f"  TITLE = {title},", f"  AUTHOR = {{{author}}},", f"  JOURNAL = {{{latex_escape(journal)}}},", f"  YEAR = {{{year}}},"]
        if p.get("publisher"):
            lines.append(f"  PUBLISHER = {{{latex_escape(p['publisher'])}}},")
        if note:
            lines.append(f"  note = {{{note}}},")
        lines.append("}")
        bib_entries.append("\n".join(lines))

    # Theses
    for t in pub.get("theses", []):
        key = t["bib_key"]
        school = latex_escape(t.get("school", ""))
        title = "{{" + latex_escape(t["title"]) + "}}"
        year = t["year"]
        if "Ph.D" in t.get("venue", "") or "phd" in key.lower():
            lines = [f"@phdthesis{{{key},", f"  AUTHOR = {{Jacquet, Pierre}},", f"  title   = {title},", f"  school  = {{{school}}},", f"  year    = {{{year}}}", "}"]
        else:
            lines = [f"@mastersthesis{{{key},", f"  AUTHOR = {{Jacquet, Pierre}},", f"  title   = {title},", f"  school  = {{{school}}},", f"  year    = {{{year}}}", "}"]
        bib_entries.append("\n".join(lines))

    # Interviews -> @misc
    for i in interviews.get("interviews", []):
        key = i["bib_key"]
        title = "{{" + latex_escape(i["title"]) + "}}"
        raw = i.get("authors", "")
        authors = latex_escape(raw.replace("Pierre Jacquet", "Jacquet, Pierre").replace("P. Jacquet", "Jacquet, Pierre"))
        year = i["year"]
        note = i.get("note", "")
        if note.startswith("http"):
            note = f"\\newline\\url{{{latex_escape_url(note)}}}"
        else:
            note = latex_escape(note)
        lines = [f"@misc{{{key},", f"  TITLE = {title},", f"  AUTHOR = {{{authors}}},", f"  YEAR = {{{year}}},", f"  note = {{{note}}}", "}"]
        bib_entries.append("\n".join(lines))

    return "\n\n".join(bib_entries)


def generate_publications_main(pub):
    papers = [p for p in pub.get("papers", []) if p.get("section") == "main"]
    return "\n".join(f"\\pubitem \\bibentry{{{p['bib_key']}}}" for p in papers)


def generate_publications_workshop(pub):
    papers = [p for p in pub.get("papers", []) if p.get("section") == "workshop"]
    return "\n".join(f"\\pubitem \\bibentry{{{p['bib_key']}}}" for p in papers)


def generate_publications_thesis(pub):
    theses = pub.get("theses", [])
    if not theses:
        return ""
    # No \\ after items: thesislist environment does not accept line break there
    return "\n".join(f"\\item  \\bibentry{{{t['bib_key']}}}" for t in theses)


def generate_service_section(service):
    categories = service.get("categories", [])
    out = []
    for i, cat in enumerate(categories):
        name = cat["name"]
        if name == "Committees":
            label = "Comittees"
        elif name == "Reviews":
            label = "Reviews"
        else:
            label = name
        # \hfill \break before new subsections (no \\ on last list item)
        if i > 0:
            if name == "Organization":
                out.append("\\textit{* Sub-reviewing}\\newline")
            out.append("\\hfill \\break")
        out.append(f"\\textbf{{{label}:}}\\newline")
        out.append("\\begin{itemize}")
        for item in cat.get("items", []):
            text = latex_escape(item.get("text", ""))
            link = item.get("link")
            suffix = (item.get("suffix") or "").strip()
            years = item.get("years")
            year_str = (" " + ", ".join(str(y) for y in years)) if years else ""
            if link:
                link_label = latex_escape(link["label"])
                # Committees: suffix and years go inside link label (e.g. "IEEE Cluster 2026")
                if name != "Organization" and (suffix or years):
                    if suffix:
                        link_label = link_label + " " + suffix
                    if years:
                        link_label = link_label + year_str
                link_tex = f"\\href{{{latex_escape_url(link['url'])}}}{{{link_label}}}"
                if name == "Organization" and suffix:
                    out.append(f"    \\item {text}{link_tex} {suffix}")
                else:
                    out.append(f"    \\item {text}{link_tex}")
            else:
                out.append(f"    \\item {text}{suffix}{year_str}")
        out.append("\\end{itemize}")
    return "\n".join(out)


def generate_talks_section(talks_data):
    talks = talks_data.get("talks", [])
    # Use order from file (newest first in current data)
    lines = []
    for t in talks:
        title = t.get("title", "")
        venue = t.get("venue", "")
        location = t.get("location", "")
        year = t.get("year", "")
        note = t.get("note", "")
        links = t.get("links", [])
        # Prefer link with label that could be the main event link (Schedule, Event, Meeting, Slides)
        url = get_first_link_url(links)
        if url and links and links[0].get("label") in ("Schedule", "Event", "Meeting", "Slides", "Video"):
            title_tex = f"\\textit{{\\href{{{latex_escape_url(url)}}}{{{latex_escape(title)}}}}}"
        else:
            title_tex = f"\\textit{{{latex_escape(title)}}}"
        loc_short = location.replace("Canada", "Canada").replace("France", "France").replace("Norway", "Norway").replace("Norvège", "Norway").replace("Germany", "Germany").replace("Allemagne", "Germany")
        if "Montréal" in location or "Canada" in location:
            loc_short = "Canada"
        elif "France" in location or "Lyon" in location or "Paris" in location or "Toulouse" in location or "Nantes" in location or "Rennes" in location or "en ligne" in location:
            loc_short = "France"
        elif "Norway" in location or "Norvège" in location:
            loc_short = "Norway"
        elif "Germany" in location or "Allemagne" in location or "Munich" in location:
            loc_short = "Germany"
        else:
            loc_short = location
        line = f"{title_tex}, {latex_escape(venue)} ({loc_short}, {year})"
        if note:
            line += f" — {note}"
        lines.append(line + "\\\\")
    return "\n".join(lines)


def generate_artifacts_section(artifacts_data):
    artifacts = artifacts_data.get("artifacts", [])
    lines = []
    for a in artifacts:
        name = latex_escape(a["name"])
        family = a.get("family", "")
        audience = a.get("audience", "")
        evolution = a.get("evolution", "")
        duration = a.get("duration", "")
        contribution = a.get("contribution", "")
        url = a.get("url", "")
        desc = latex_escape(a.get("description", ""))
        lines.append(f"\\item {name}.  ")
        lines.append(f"\\textit{{Family}}: {family}; ")
        lines.append(f"\\textit{{Audience}}: {audience}; ")
        lines.append(f"\\textit{{Evolution}}: {evolution}; ")
        lines.append(f"\\textit{{Duration}}: {duration}; ")
        lines.append(f"\\textit{{Contribution}}: {contribution}; ")
        lines.append(f"\\textit{{URL}}: \\url{{{latex_escape_url(url)}}}.  ")
        lines.append("")
        lines.append(desc)
        lines.append("")
    return "\n".join(lines)


def generate_outreach_interviews(interviews_data):
    items = interviews_data.get("interviews", [])
    # Use \par to separate entries; \\ causes "There's no line here to end" in this context
    return "\\par\n".join(f"\\bibentry{{{i['bib_key']}}}" for i in items)


def generate_outreach_press(pub):
    press = pub.get("press", [])
    # Use \par to separate entries; \\ causes "There's no line here to end" in this context
    return "\\par\n".join(f"\\bibentry{{{p['bib_key']}}}" for p in press)


def main():
    os.chdir(REPO_ROOT)
    pub = load_yaml("publications")
    service = load_yaml("service")
    talks_data = load_yaml("talks")
    artifacts_data = load_yaml("artifacts")
    interviews_data = load_yaml("interviews")

    # Generate cv.bib
    bib_content = generate_bib()
    with open(OUT_BIB_PATH, "w", encoding="utf-8") as f:
        f.write(bib_content)
    print(f"Wrote {OUT_BIB_PATH}")

    # Placeholders for skeleton
    replacements = {
        "{{PUBLICATIONS_MAIN}}": generate_publications_main(pub),
        "{{PUBLICATIONS_WORKSHOP}}": generate_publications_workshop(pub),
        "{{PUBLICATIONS_THESIS}}": generate_publications_thesis(pub),
        "{{SERVICE_SECTION}}": generate_service_section(service),
        "{{OUTREACH_TALKS}}": generate_talks_section(talks_data),
        "{{ARTIFACTS_SECTION}}": generate_artifacts_section(artifacts_data),
        "{{OUTREACH_INTERVIEWS}}": generate_outreach_interviews(interviews_data),
        "{{OUTREACH_PRESS}}": generate_outreach_press(pub),
    }

    with open(SKELETON_PATH, encoding="utf-8") as f:
        tex = f.read()
    for placeholder, value in replacements.items():
        tex = tex.replace(placeholder, value)
    with open(OUT_TEX_PATH, "w", encoding="utf-8") as f:
        f.write(tex)
    print(f"Wrote {OUT_TEX_PATH}")


if __name__ == "__main__":
    main()
