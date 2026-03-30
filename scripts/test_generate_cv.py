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


# --- generate_service_section: typed entries and formatting ---


def test_generate_service_sub_reviewing():
    """Typed sub-reviewing entries are listed without legacy star legend."""
    service = {
        "entries": [
            {"domain": "journal", "role_type": "Reviewer", "role_group": "reviewer", "venue": "Journal A"},
            {
                "domain": "journal/conference",
                "role_type": "Sub-reviewer",
                "role_group": "sub_reviewer",
                "venue": "IEEE Internet Computing",
                "sub_reviewing": True,
            },
        ]
    }
    out = gen.generate_service_section(service)
    assert "Journal - Reviewer" in out
    assert "Journal - Sub-reviewer" in out
    assert "Journal A" in out
    assert "IEEE Internet Computing" in out
    assert "~*" not in out
    assert "* Sub-reviewing" not in out


def test_generate_service_conference_reviewer_group():
    """Conference reviewer entries appear in Conference - Reviewer."""
    service = {
        "entries": [
            {"domain": "conference", "role_type": "Reviewer", "role_group": "reviewer", "venue": "GreenNet Workshop", "year": 2025},
        ]
    }
    out = gen.generate_service_section(service)
    assert "Conference - Reviewer" in out
    assert "GreenNet Workshop 2025" in out
    assert "Journal - Reviewer" not in out


def test_generate_service_organization_group():
    """Organization entries are rendered when present."""
    service = {
        "entries": [
            {
                "domain": "organization",
                "role_type": "Volunteer",
                "role_group": "volunteer",
                "venue": "IEEE ICC",
                "year": 2025,
            }
        ]
    }
    out = gen.generate_service_section(service)
    assert "Organization" in out
    assert "IEEE ICC 2025" in out


def test_generate_service_note_after_only_when_sub_reviewing():
    """No legacy sub-reviewing legend is rendered."""
    service = {
        "entries": [
            {"domain": "journal/conference", "role_type": "Sub-reviewer", "role_group": "sub_reviewer", "venue": "Journal X"},
        ]
    }
    out = gen.generate_service_section(service)
    assert "* Sub-reviewing" not in out


def test_generate_service_no_whitespace_hack_needed():
    """Service formatting is deterministic without relying on trailing spaces."""
    service = {
        "entries": [
            {
                "domain": "conference",
                "role_type": "PC Member",
                "role_group": "pc_member",
                "venue": "IEEE Cluster",
                "url": "https://cluster.example",
                "note": "  Workshop  ",
                "years": [2025, 2026],
            }
        ]
    }
    out = gen.generate_service_section(service)
    assert "\\href{https://cluster.example}{IEEE Cluster (Workshop) 2025, 2026}" in out


def test_generate_service_entry_role_prefix_is_explicit():
    service = {
        "entries": [
            {
                "domain": "conference",
                "role_type": "General Chair",
                "role_group": "general_chair",
                "role_prefix": "Web Chair",
                "venue": "INFRASTRUCTURE",
                "year": 2026,
            }
        ]
    }
    out = gen.generate_service_section(service)
    assert "Conference - General Chair" in out
    assert "Web Chair: INFRASTRUCTURE 2026" in out


def test_generate_service_custom_role_type_with_explicit_group_renders():
    service = {
        "entries": [
            {
                "domain": "conference",
                "role_type": "Mentor",
                "role_group": "reviewer",
                "venue": "Community Event",
                "year": 2025,
            }
        ]
    }
    out = gen.generate_service_section(service)
    assert "Conference - Reviewer" in out
    assert "Community Event 2025" in out


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
                "month_num": 6,
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
    assert "Conf, Paris, France, June, 2025" in out


def test_generate_talks_includes_month_in_meta_line():
    talks_data = {
        "talks": [
            {
                "title": "T",
                "venue": "Venue",
                "location": "Here",
                "year": 2025,
                "month_num": 11,
            }
        ]
    }
    out = gen.generate_talks_section(talks_data)
    assert "November" in out
    assert "Venue, Here, November, 2025" in out


def test_generate_talks_sorted_by_year_month_preserves_tie_order():
    talks_data = {
        "talks": [
            {"title": "AprilTalk", "venue": "V", "year": 2025, "month_num": 4},
            {"title": "OctoberTalk", "venue": "V", "year": 2025, "month_num": 10},
            {"title": "JuneA", "venue": "V", "year": 2024, "month_num": 6},
            {"title": "JuneB", "venue": "V", "year": 2024, "month_num": 6},
        ]
    }
    out = gen.generate_talks_section(talks_data)
    assert out.index("OctoberTalk") < out.index("AprilTalk")
    assert out.index("AprilTalk") < out.index("JuneA")
    assert out.index("JuneA") < out.index("JuneB")


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
