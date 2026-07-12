#!/usr/bin/env python3
"""
05_build_references.py
======================
Build IEEE-formatted bibliography, BibTeX file, and high-impact
paper list from the GNSS-Denied Drone Localization SLR database.

Reads  : data/processed/database_final.csv
Writes : references/bibliography.txt
         references/references.bib
         references/key_papers.md

Author : SLR Pipeline
Date   : 2026-07-12
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

# Fix Windows console encoding for Unicode output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Resolve project root ────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "database_final.csv"
BIB_TXT = BASE_DIR / "references" / "bibliography.txt"
BIB_TEX = BASE_DIR / "references" / "references.bib"
KEY_PAPERS = BASE_DIR / "references" / "key_papers.md"

# ── Top-tier venue keywords for high-impact detection ───────────────
TOP_VENUES = [
    "ieee transactions",
    "ieee trans.",
    "ieee robotics and automation letters",
    "ieee ra-l",
    "ra-l",
    "icra",
    "iros",
    "sensors",
    "ieee access",
    "journal of field robotics",
    "autonomous robots",
    "robotics and autonomous systems",
    "ieee aerospace",
    "international journal of",
    "ieee/asme transactions",
    "navigation",
    "journal of intelligent",
]

CONFERENCE_MARKERS = [
    "conference", "symposium", "workshop", "proceedings",
    "congress", "convention", "meeting", "icra", "iros",
    "iccv", "cvpr", "eccv",
]


# ── Author name formatting ──────────────────────────────────────────

def _strip_accents(s: str) -> str:
    """Remove accent marks for BibTeX key generation."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def _parse_single_author(name: str) -> tuple[str, str]:
    """
    Parse a single author name and return (first_names, last_name).
    Handles formats like:
       'Last, First Middle'
       'First Middle Last'
    """
    name = name.strip().rstrip(".")
    if not name:
        return ("", "")

    # Handle "Last, First" format
    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        last = parts[0]
        first = parts[1] if len(parts) > 1 else ""
        return (first, last)

    # Handle "First Middle Last" format
    tokens = name.split()
    if len(tokens) == 1:
        return ("", tokens[0])
    last = tokens[-1]
    first = " ".join(tokens[:-1])
    return (first, last)


def format_author_ieee(name: str) -> str:
    """
    Format a single author as 'F. M. Last' for IEEE style.
    """
    first, last = _parse_single_author(name)
    if not last:
        return name.strip()
    if not first:
        return last

    # Build initials
    initials = []
    for part in first.split():
        if part:
            initials.append(f"{part[0].upper()}.")
    return " ".join(initials) + " " + last


def format_authors_ieee(authors_str: str) -> str:
    """
    Format the full author list for IEEE citation.
    If >3 authors, use 'First Author et al.'
    """
    if not isinstance(authors_str, str) or not authors_str.strip():
        return "Unknown Author"

    # Split on ';' (common in exported CSV)
    authors = [a.strip() for a in authors_str.split(";") if a.strip()]
    if not authors:
        return "Unknown Author"

    formatted = [format_author_ieee(a) for a in authors]

    if len(formatted) > 3:
        return f"{formatted[0]} et al."
    elif len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]} and {formatted[1]}"
    else:  # 3
        return f"{formatted[0]}, {formatted[1]}, and {formatted[2]}"


def format_authors_bibtex(authors_str: str) -> str:
    """
    Format authors for BibTeX: 'Last, First and Last, First'.
    """
    if not isinstance(authors_str, str) or not authors_str.strip():
        return "Unknown Author"

    authors = [a.strip() for a in authors_str.split(";") if a.strip()]
    bib_authors = []
    for a in authors:
        first, last = _parse_single_author(a)
        if first:
            bib_authors.append(f"{last}, {first}")
        else:
            bib_authors.append(last)
    return " and ".join(bib_authors)


# ── BibTeX key generation ───────────────────────────────────────────

def make_bibtex_key(authors_str: str, year) -> str:
    """
    Generate a BibTeX key: lowercase first-author-last-name + year.
    """
    if not isinstance(authors_str, str) or not authors_str.strip():
        first_author = "unknown"
    else:
        first = authors_str.split(";")[0].strip()
        _, last = _parse_single_author(first)
        first_author = _strip_accents(last).lower()
        first_author = re.sub(r"[^a-z]", "", first_author)
        if not first_author:
            first_author = "unknown"

    yr = str(int(year)) if pd.notna(year) else "0000"
    return f"{first_author}{yr}"


def is_conference(publication: str) -> bool:
    """Return True if the publication name looks like a conference."""
    if not isinstance(publication, str):
        return False
    pub_lower = publication.lower()
    return any(m in pub_lower for m in CONFERENCE_MARKERS)


# ── Escape LaTeX special characters in BibTeX ───────────────────────

def escape_bibtex(text: str) -> str:
    """Minimally escape special characters for BibTeX values."""
    if not isinstance(text, str):
        return ""
    # Protect '&' and '%' which are common
    text = text.replace("&", r"\&")
    text = text.replace("%", r"\%")
    return text


# ── IEEE citation builder ───────────────────────────────────────────

def build_ieee_citation(row: pd.Series, ref_num: int) -> str:
    """
    Build an IEEE-format numbered citation string.
    Format:
      [N] Authors, "Title," Publication, Year. doi:DOI
    """
    parts: list[str] = []

    # Authors
    authors = format_authors_ieee(row.get("authors", ""))
    parts.append(f"[{ref_num}] {authors}")

    # Title
    title = str(row.get("title", "Untitled")).strip()
    parts.append(f', "{title},"')

    # Publication venue
    pub = str(row.get("publication", "")).strip() if pd.notna(row.get("publication")) else ""
    if pub:
        parts.append(f" *{pub}*,")

    # Year
    year = row.get("year", "")
    if pd.notna(year):
        parts.append(f" {int(year)}.")
    else:
        parts.append(".")

    # DOI
    doi = str(row.get("doi", "")).strip() if pd.notna(row.get("doi")) else ""
    if doi:
        parts.append(f" doi:{doi}")

    return "".join(parts)


# ── BibTeX entry builder ────────────────────────────────────────────

def build_bibtex_entry(row: pd.Series, key: str) -> str:
    """Build a single BibTeX entry."""
    pub = str(row.get("publication", "")).strip() if pd.notna(row.get("publication")) else ""
    entry_type = "@inproceedings" if is_conference(pub) else "@article"

    lines = [f"{entry_type}{{{key},"]

    # author
    bib_auth = format_authors_bibtex(row.get("authors", ""))
    lines.append(f"  author = {{{escape_bibtex(bib_auth)}}},")

    # title
    title = str(row.get("title", "")).strip()
    lines.append(f"  title = {{{escape_bibtex(title)}}},")

    # journal / booktitle
    if entry_type == "@article":
        lines.append(f"  journal = {{{escape_bibtex(pub)}}},")
    else:
        lines.append(f"  booktitle = {{{escape_bibtex(pub)}}},")

    # year
    year = row.get("year", "")
    if pd.notna(year):
        lines.append(f"  year = {{{int(year)}}},")

    # doi
    doi = str(row.get("doi", "")).strip() if pd.notna(row.get("doi")) else ""
    if doi:
        lines.append(f"  doi = {{{doi}}},")

    # issn
    issn = str(row.get("issn", "")).strip() if pd.notna(row.get("issn")) else ""
    if issn:
        lines.append(f"  issn = {{{issn}}},")

    lines.append("}")
    return "\n".join(lines)


# ── High-impact detection ───────────────────────────────────────────

def is_high_impact(row: pd.Series) -> bool:
    """
    Return True if the paper is considered high-impact:
      - citation_count >= 10, OR
      - published in a top-tier venue
    """
    # Citation threshold
    cite = row.get("citation_count", 0)
    if pd.notna(cite) and float(cite) >= 10:
        return True

    # Venue check
    pub = str(row.get("publication", "")).lower() if pd.notna(row.get("publication")) else ""
    for kw in TOP_VENUES:
        if kw in pub:
            return True

    return False


# ═══════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("  GNSS-Denied Drone SLR — Reference Builder Pipeline")
    print("=" * 65)

    # ── Load ────────────────────────────────────────────────────────
    if not DATA_PATH.exists():
        sys.exit(f"[✗] Data file not found: {DATA_PATH}")

    print(f"\n[•] Loading {DATA_PATH.relative_to(BASE_DIR)} …")
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    print(f"    Loaded {len(df)} papers.")

    # ── Sort: year ascending, then first author alphabetically ──────
    df["_sort_author"] = df["authors"].fillna("ZZZ").str.split(";").str[0].str.strip().str.lower()
    df["_sort_year"] = df["year"].fillna(9999).astype(int)
    df = df.sort_values(["_sort_year", "_sort_author"]).reset_index(drop=True)

    # ── Ensure unique BibTeX keys ───────────────────────────────────
    key_counter: dict[str, int] = {}
    bibtex_keys: list[str] = []
    for _, row in df.iterrows():
        base_key = make_bibtex_key(row.get("authors", ""), row.get("year", 0))
        key_counter[base_key] = key_counter.get(base_key, 0) + 1
        if key_counter[base_key] == 1:
            bibtex_keys.append(base_key)
        else:
            # Append a/b/c/… suffix for duplicates
            suffix = chr(ord("a") + key_counter[base_key] - 1)
            bibtex_keys.append(f"{base_key}{suffix}")
    df["_bib_key"] = bibtex_keys

    # ── Build IEEE bibliography ─────────────────────────────────────
    print("\n[•] Building IEEE bibliography …")
    BIB_TXT.parent.mkdir(parents=True, exist_ok=True)

    citations: list[str] = []
    for i, (_, row) in enumerate(df.iterrows(), 1):
        citations.append(build_ieee_citation(row, i))

    BIB_TXT.write_text("\n\n".join(citations), encoding="utf-8")
    print(f"    → Saved {len(citations)} citations to {BIB_TXT.relative_to(BASE_DIR)}")

    # ── Build BibTeX file ───────────────────────────────────────────
    print("\n[•] Building BibTeX file …")
    bib_entries: list[str] = []
    for _, row in df.iterrows():
        entry = build_bibtex_entry(row, row["_bib_key"])
        bib_entries.append(entry)

    header = (
        "% ============================================================\n"
        "% GNSS-Denied Drone Localization — Systematic Literature Review\n"
        f"% Auto-generated BibTeX — {len(bib_entries)} entries\n"
        "% ============================================================\n\n"
    )
    BIB_TEX.write_text(header + "\n\n".join(bib_entries), encoding="utf-8")
    print(f"    → Saved {len(bib_entries)} entries to {BIB_TEX.relative_to(BASE_DIR)}")

    # ── High-impact papers ──────────────────────────────────────────
    print("\n[•] Identifying high-impact papers …")
    df["_high_impact"] = df.apply(is_high_impact, axis=1)
    hi_df = df[df["_high_impact"]].copy()
    print(f"    High-impact papers: {len(hi_df)} / {len(df)}")

    # Build key_papers.md
    md_lines: list[str] = [
        "# Key / High-Impact Papers\n",
        f"**Total**: {len(hi_df)} papers identified as high-impact.\n",
        "**Criteria**: citation count ≥ 10 OR published in a recognised "
        "top-tier venue (IEEE Transactions, RA-L, ICRA, IROS, Sensors, etc.)\n",
        "---\n",
    ]

    # Sort high-impact by citation count descending
    cite_col = "citation_count"
    if cite_col in hi_df.columns:
        hi_df = hi_df.sort_values(cite_col, ascending=False)

    md_lines.append("| # | Year | Citations | Title | Venue | DOI |")
    md_lines.append("|--:|-----:|----------:|-------|-------|-----|")
    for i, (_, row) in enumerate(hi_df.iterrows(), 1):
        yr = int(row["year"]) if pd.notna(row.get("year")) else ""
        cites = int(row[cite_col]) if pd.notna(row.get(cite_col)) else 0
        title = str(row.get("title", "")).strip()[:80]
        pub = str(row.get("publication", "")).strip()[:50] if pd.notna(row.get("publication")) else ""
        doi = str(row.get("doi", "")).strip() if pd.notna(row.get("doi")) else ""
        md_lines.append(f"| {i} | {yr} | {cites} | {title} | {pub} | {doi} |")

    KEY_PAPERS.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"    → Saved: {KEY_PAPERS.relative_to(BASE_DIR)}")

    # ── Top 10 most cited ───────────────────────────────────────────
    print("\n[•] Top 10 most cited papers:")
    if cite_col in df.columns:
        top10 = df.nlargest(10, cite_col)
        for i, (_, row) in enumerate(top10.iterrows(), 1):
            cites = int(row[cite_col]) if pd.notna(row[cite_col]) else 0
            title = str(row.get("title", ""))[:70]
            yr = int(row["year"]) if pd.notna(row.get("year")) else "?"
            print(f"    {i:2d}. [{cites:4d} cites] ({yr}) {title}")
    else:
        print("    'citation_count' column not found — skipping top-cited list.")

    # ── Entry type breakdown ────────────────────────────────────────
    n_conf = sum(1 for _, r in df.iterrows()
                 if is_conference(str(r.get("publication", ""))))
    n_jour = len(df) - n_conf

    # ── Final summary ──────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  Summary")
    print("=" * 65)
    print(f"  Total references        : {len(df)}")
    print(f"  Journal articles        : {n_jour}")
    print(f"  Conference papers       : {n_conf}")
    print(f"  High-impact papers      : {len(hi_df)}")
    print(f"  Bibliography            : {BIB_TXT.relative_to(BASE_DIR)}")
    print(f"  BibTeX                  : {BIB_TEX.relative_to(BASE_DIR)}")
    print(f"  Key papers              : {KEY_PAPERS.relative_to(BASE_DIR)}")
    print("=" * 65)

    # Clean up temp columns
    df.drop(columns=["_sort_author", "_sort_year", "_bib_key", "_high_impact"],
            inplace=True, errors="ignore")


if __name__ == "__main__":
    main()
