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


def normalize_role_group(item):
    """
    Resolve the grouping key for a service entry.
    Prefer explicit role_group, with a backward-compatible fallback to role_type.
    """
    role_group = item.get("role_group")
    if role_group is not None and str(role_group).strip():
        return str(role_group).strip().lower()
    role_type = item.get("role_type")
    if role_type is None:
        return ""
    return re.sub(r"_+", "_", str(role_type).strip().lower().replace("-", "_").replace(" ", "_")).strip("_")


_MONTH_LABELS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def _month_num_to_sort_num(month_num):
    """Map optional month_num field to 1–12; 0 = missing/unknown."""
    if month_num is None or month_num == "":
        return 0
    try:
        mn = int(month_num)
    except (TypeError, ValueError):
        return 0
    return mn if 1 <= mn <= 12 else 0


def _month_num_to_label(month_num):
    """Map month_num to display month label."""
    mn = _month_num_to_sort_num(month_num)
    return _MONTH_LABELS.get(mn, "")


def _is_true(value):
    """Interpret booleans from YAML and common string/int forms."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return False


def _sort_talks_list(talks):
    """Reverse chronological by year then month; ties keep YAML file order."""

    def sort_key(ie):
        i, t = ie
        y = t.get("year")
        try:
            yi = int(y)
        except (TypeError, ValueError):
            yi = 0
        mn = _month_num_to_sort_num(t.get("month_num"))
        return (-yi, -mn, i)

    return [t for _, t in sorted(enumerate(talks), key=sort_key)]


def generate_bib(pub=None, interviews=None):
    """Generate bib content. If pub/interviews are None, load from data/ (allows injecting data in tests)."""
    if pub is None:
        pub = load_yaml("publications")
    if interviews is None:
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
        publisher = latex_escape(p.get("publisher", "IEEE"))
        lines.append(f"  PUBLISHER = {{{publisher}}},")
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
        thesis_type = (t.get("thesis_type") or "phd").lower()
        if thesis_type == "masters":
            lines = [f"@mastersthesis{{{key},", f"  AUTHOR = {{Jacquet, Pierre}},", f"  title   = {title},", f"  school  = {{{school}}},", f"  year    = {{{year}}}", "}"]
        else:
            lines = [f"@phdthesis{{{key},", f"  AUTHOR = {{Jacquet, Pierre}},", f"  title   = {title},", f"  school  = {{{school}}},", f"  year    = {{{year}}}", "}"]
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
    papers = [p for p in pub.get("papers", []) if p.get("section_cv") == "main"]
    return "\n".join(f"\\pubitem \\bibentry{{{p['bib_key']}}}" for p in papers)


def generate_publications_workshop(pub):
    papers = [p for p in pub.get("papers", []) if p.get("section_cv") == "workshop"]
    return "\n".join(f"\\pubitem \\bibentry{{{p['bib_key']}}}" for p in papers)


def generate_publications_thesis(pub):
    theses = pub.get("theses", [])
    if not theses:
        return ""
    # No \\ after items: thesislist environment does not accept line break there
    return "\n".join(f"\\item  \\bibentry{{{t['bib_key']}}}" for t in theses)


def generate_service_section(service):
    entries = service.get("entries", [])
    groups = [
        ({"conference"}, {"pc_member", "pc_chair"}, "Conference - PC Member", ""),
        ({"conference"}, {"artifact_pc_member", "artifact_chair"}, "Conference - Artifact PC Member", ""),
        ({"conference"}, {"general_chair"}, "Conference - General Chair", ""),
        ({"conference", "journal/conference"}, {"reviewer"}, "Conference - Reviewer", ""),
        ({"journal"}, {"reviewer", "editor"}, "Journal - Reviewer", ""),
        ({"journal", "journal/conference"}, {"sub_reviewer"}, "Journal - Sub-reviewer", ""),
        ({"organization"}, {"volunteer", "chair", "other"}, "Organization", ""),
    ]

    out = []
    visible_groups = []
    for domains, role_groups, label, note_after in groups:
        group_items = [
            item
            for item in entries
            if item.get("domain") in domains
            and normalize_role_group(item) in role_groups
        ]
        if group_items:
            visible_groups.append((label, group_items, note_after))

    for i, (label, group_items, note_after) in enumerate(visible_groups):
        if i > 0:
            out.append("\\hfill \\break")
        out.append(f"\\textbf{{{latex_escape(label)}:}}\\newline")
        out.append("\\begin{itemize}")
        for item in group_items:
            venue = latex_escape(item.get("venue", ""))
            url = (item.get("url") or "").strip()
            note = (item.get("note") or "").strip()
            years = item.get("years")
            year = item.get("year")
            if years:
                year_text = ", ".join(str(y) for y in years)
            elif year is not None and year != "":
                year_text = str(year)
            else:
                year_text = ""

            label_text = venue
            role_prefix = (item.get("role_prefix") or "").strip()
            if role_prefix:
                label_text = f"{latex_escape(role_prefix)}: {label_text}"
            if note:
                label_text += f" ({latex_escape(note)})"
            if year_text:
                label_text += f" {latex_escape(year_text)}"

            if url:
                item_text = f"\\href{{{latex_escape_url(url)}}}{{{label_text}}}"
            else:
                item_text = label_text

            out.append(f"    \\item {item_text}")

        out.append("\\end{itemize}")
        if note_after:
            out.append(f"\\textit{{{latex_escape(note_after)}}}\\newline")

    return "\n".join(out)


def generate_talks_section(talks_data):
    talks = _sort_talks_list(list(talks_data.get("talks", [])))
    lines = []
    for t in talks:
        title = t.get("title", "")
        talk_type = (t.get("type") or "").strip()
        venue = t.get("venue", "")
        location = (t.get("location") or "").strip()
        month_label = _month_num_to_label(t.get("month_num"))
        year = t.get("year", "")
        note = (t.get("note") or "").strip()
        links = t.get("links") or []

        title_esc = latex_escape(title)
        link_parts = []
        for link in links:
            url = (link.get("url") or "").strip()
            label = (link.get("label") or "").strip()
            if url and label:
                link_parts.append(
                    f"\\href{{{latex_escape_url(url)}}}{{{latex_escape(label)}}}"
                )
        if link_parts:
            title_line = f"\\textit{{{title_esc}}} ~ " + ", ".join(link_parts)
        else:
            title_line = f"\\textit{{{title_esc}}}"

        if talk_type and _is_true(t.get("highlighted", False)):
            type_tex = f"\\textbf{{{latex_escape(talk_type)}}}"
        elif talk_type:
            type_tex = latex_escape(talk_type)
        else:
            type_tex = ""

        loc_tex = latex_escape(location) if location else ""
        meta_parts = []
        if type_tex:
            meta_parts.append(type_tex)
        meta_parts.append(latex_escape(venue))
        if loc_tex:
            meta_parts.append(loc_tex)
        if month_label:
            meta_parts.append(latex_escape(month_label))
        if year != "" and year is not None:
            meta_parts.append(str(year))
        meta_line = ", ".join(meta_parts)
        if note:
            meta_line += f" — {latex_escape(note)}"

        lines.append(f"    \\item {title_line}\\\\\n    {meta_line}")
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
    bib_content = generate_bib(pub=pub, interviews=interviews_data)
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
