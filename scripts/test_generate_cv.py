"""
Tests for generate_cv.py (same folder).
Run from repo root: pytest scripts/test_generate_cv.py -v
"""
import sys
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
import generate_cv as gen


# --- latex_escape ---


def test_latex_escape_empty():
    assert gen.latex_escape("") == ""
    assert gen.latex_escape(None) is None


def test_latex_escape_special_chars():
    assert "\\&" in gen.latex_escape("a & b")
    assert "\\%" in gen.latex_escape("50%")
    assert "\\#" in gen.latex_escape("#tag")
    assert "\\_" in gen.latex_escape("a_b")


def test_latex_escape_accents():
    assert "{\\'e}" in gen.latex_escape("café")
    assert "{\\`e}" in gen.latex_escape("è")
    assert "{\\c c}" in gen.latex_escape("ça")


# --- bib_author ---


def test_bib_author_bolds_pierre_first():
    s = "Pierre Jacquet, Camille Coti, and Romain Rouvoy"
    out = gen.bib_author(s)
    assert "\\textbf{Jacquet}, \\textbf{Pierre}" in out
    assert "Camille Coti" in out


def test_bib_author_bolds_pierre_not_first():
    s = "Alice A, Pierre Jacquet, and Bob B"
    out = gen.bib_author(s)
    assert "\\textbf{Jacquet}, \\textbf{Pierre}" in out
    assert "Alice A" in out and "Bob B" in out


def test_bib_author_bolds_p_dot_jacquet():
    out = gen.bib_author("P. Jacquet, Other Author")
    assert "\\textbf{Jacquet}, \\textbf{Pierre}" in out


def test_bib_author_no_bold_when_disabled():
    out = gen.bib_author("Pierre Jacquet, Other", bold_me=False)
    assert "\\textbf" not in out
    assert "Pierre Jacquet" in out


def test_bib_author_empty():
    assert gen.bib_author("") == ""


def test_bib_author_strips_and_from_parts():
    out = gen.bib_author("A, B, and C")
    assert " and and " not in out
    assert out == "A and B and C"


# --- format_venue_red ---


def test_format_venue_red_with_abbr():
    out = gen.format_venue_red("European Conference on X", "EuroSys")
    assert "EuroSys" in out
    assert "red" in out or "textcolor" in out.lower()


def test_format_venue_red_no_abbr():
    out = gen.format_venue_red("Some Venue", "")
    assert "Some Venue" in out


# --- generate_bib: publisher from data ---


def test_generate_bib_publisher_from_data():
    pub = {
        "papers": [
            {
                "bib_key": "testacm",
                "title": "Test",
                "authors": "Pierre Jacquet",
                "venue": "ACM Conf",
                "year": 2025,
                "entry_type": "conference",
                "publisher": "ACM",
            },
            {
                "bib_key": "testieee",
                "title": "Test IEEE",
                "authors": "Pierre Jacquet",
                "venue": "IEEE Conf",
                "year": 2025,
                "entry_type": "conference",
            },
        ],
        "press": [],
        "theses": [],
    }
    interviews = {"interviews": []}
    bib = gen.generate_bib(pub=pub, interviews=interviews)
    assert "PUBLISHER = {ACM}" in bib
    assert "PUBLISHER = {IEEE}" in bib


# --- generate_bib: thesis_type from data ---


def test_generate_bib_thesis_type_phd():
    pub = {
        "papers": [],
        "press": [],
        "theses": [
            {
                "bib_key": "phd",
                "title": "My PhD",
                "school": "Univ",
                "year": 2024,
                "thesis_type": "phd",
            }
        ],
    }
    bib = gen.generate_bib(pub=pub, interviews={"interviews": []})
    assert "@phdthesis{phd" in bib


def test_generate_bib_thesis_type_masters():
    pub = {
        "papers": [],
        "press": [],
        "theses": [
            {
                "bib_key": "ms",
                "title": "My Masters",
                "school": "Univ",
                "year": 2022,
                "thesis_type": "masters",
            }
        ],
    }
    bib = gen.generate_bib(pub=pub, interviews={"interviews": []})
    assert "@mastersthesis{ms" in bib


# --- generate_service_section: note_after and sub_reviewing ---


def test_generate_service_sub_reviewing():
    """Items with sub_reviewing: true get ~* in CV output; others do not."""
    service = {
        "categories": [
            {
                "name": "Reviews",
                "note_after": "* Sub-reviewing",
                "items": [
                    {"text": "Journal A"},
                    {"text": "IEEE Internet Computing", "sub_reviewing": True},
                ],
            }
        ]
    }
    out = gen.generate_service_section(service)
    assert "Journal A" in out
    assert "~*" not in out.split("Journal A")[0]  # first item has no *
    assert "IEEE Internet Computing" in out
    assert "~*" in out
    assert "* Sub-reviewing" in out


def test_generate_service_note_after_only_when_sub_reviewing():
    """Legend note_after is omitted when no item has sub_reviewing."""
    service = {
        "categories": [
            {"name": "Reviews", "items": [{"text": "Journal X"}], "note_after": "* Sub-reviewing"},
        ]
    }
    out = gen.generate_service_section(service)
    assert "* Sub-reviewing" not in out


# --- generate_talks_section: location as-is ---


def test_generate_talks_location_from_data():
    """Location is taken from data (no shortening); it may be LaTeX-escaped in output."""
    talks_data = {
        "talks": [
            {
                "title": "A Talk",
                "venue": "A Venue",
                "location": "Montréal, Canada",
                "year": 2025,
            }
        ]
    }
    out = gen.generate_talks_section(talks_data)
    assert "Canada" in out and "2025" in out
    assert "Montr" in out  # Montréal may appear as Montr{\'e}al


def test_generate_talks_location_other():
    talks_data = {
        "talks": [
            {
                "title": "A Talk",
                "venue": "A Venue",
                "location": "Sundvolden, Norway",
                "year": 2022,
            }
        ]
    }
    out = gen.generate_talks_section(talks_data)
    assert "Sundvolden, Norway" in out


def test_generate_talks_two_lines_keynote_and_links():
    talks_data = {
        "talks": [
            {
                "title": "My Keynote",
                "type": "Keynote",
                "venue": "Conf",
                "location": "Paris, France",
                "year": 2025,
                "links": [
                    {"label": "Slides", "url": "https://x.example/s.pdf"},
                    {"label": "Video", "url": "https://x.example/v"},
                ],
            }
        ]
    }
    out = gen.generate_talks_section(talks_data)
    assert "    \\item " in out
    assert "\\textit{My Keynote} ~ " in out
    assert "\\href{https://x.example/s.pdf}{Slides}" in out
    assert "\\textbf{Keynote}" in out
    assert "Conf, Paris, France, 2025" in out


# --- latex_escape_url ---


def test_latex_escape_url():
    assert "\\%" in gen.latex_escape_url("https://x.com?a=1%20b")
    assert "\\#" in gen.latex_escape_url("https://x.com#anchor")


# --- get_first_link_url ---


def test_get_first_link_url():
    links = [{"label": "Paper", "url": "https://a"}, {"label": "Code", "url": "https://b"}]
    assert gen.get_first_link_url(links) == "https://a"
    assert gen.get_first_link_url(links, "Code") == "https://b"
    assert gen.get_first_link_url([]) is None
