#!/usr/bin/env python3
"""
01_clean_data.py — Data Cleaning Pipeline for GNSS-Denied Drone SLR
====================================================================

This script performs the first stage of the Systematic Literature Review pipeline:
  1. Loads the raw IEEE Xplore CSV export
  2. Renames columns to clean, consistent names
  3. Cleans text fields (HTML tags, whitespace normalization)
  4. Filters by publication year (2015–2026)
  5. Parses numeric fields (citation_count, reference_count)
  6. Removes duplicates (by DOI, then by exact title match)
  7. Drops rows with empty title or abstract
  8. Applies inclusion/exclusion screening (localization/navigation focus)
  9. Creates text_corpus column for downstream NLP
  10. Prints detailed statistics and saves cleaned data

Output:
  - data/processed/database_final.csv
  - analysis/output/checkpoint1_summary.txt

Author: SLR Pipeline
Date: 2026-07-12
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Fix Windows console encoding for Unicode output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Project paths ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_CSV = BASE_DIR / "data" / "raw" / "export2026.07.12-04.50.12.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "analysis" / "output"

# Ensure output directories exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── Column renaming map ───────────────────────────────────────────────────────
COLUMN_MAP = {
    "Document Title": "title",
    "Authors": "authors",
    "Author Affiliations": "affiliations",
    "Publication Title": "publication",
    "Publication Year": "year",
    "Abstract": "abstract",
    "Author Keywords": "author_keywords",
    "IEEE Terms": "ieee_terms",
    "DOI": "doi",
    "Article Citation Count": "citation_count",
    "ISSN": "issn",
    "Funding Information": "funding",
    "Mesh_Terms": "mesh_terms",
    "Reference Count": "reference_count",
    "Publisher": "publisher",
    "Document Identifier": "document_type",
}


# ── Screening keywords (localization/navigation focus) ─────────────────────────
INCLUSION_TERMS = [
    r"\blocalization\b",
    r"\blocalisation\b",
    r"\bnavigation\b",
    r"\bslam\b",
    r"\bodometry\b",
    r"\bstate estimation\b",
    r"\bpositioning\b",
    r"\bpose estimation\b",
    r"\btrajectory\b",
    r"\bmapping\b",
    r"\bpath planning\b",
    r"\bwaypoint\b",
    r"\btracking\b",
    r"\bdead reckoning\b",
    r"\bplace recognition\b",
    r"\bloop closure\b",
    r"\brelocalization\b",
    r"\bvisual inertial\b",
    r"\bsensor fusion\b",
    r"\bmulti-sensor fusion\b",
    r"\bmulti sensor fusion\b",
    r"\binertial navigation\b",
]

# Papers that match ONLY these terms (without any inclusion term) are excluded
EXCLUSION_ONLY_TERMS = [
    r"\bcommunication\b",
    r"\bnetworking\b",
    r"\bsignal processing\b",
    r"\bspectrum\b",
]


def load_csv(filepath: Path) -> pd.DataFrame:
    """Load CSV with encoding fallback (UTF-8 → Latin-1)."""
    for encoding in ("utf-8", "latin-1"):
        try:
            df = pd.read_csv(filepath, encoding=encoding)
            print(f"  ✓ Loaded with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            print(f"  ✗ Failed with encoding: {encoding}, trying next...")
    raise RuntimeError(f"Could not read {filepath} with any supported encoding.")


def clean_text(text: str) -> str:
    """Remove HTML tags, normalize whitespace, and strip a text string."""
    if not isinstance(text, str) or pd.isna(text):
        return ""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Normalize whitespace (collapse multiple spaces/newlines/tabs)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_text_corpus(row: pd.Series) -> str:
    """Create a lowercase concatenation of key text fields for screening/NLP."""
    parts = []
    for col in ("title", "abstract", "author_keywords", "ieee_terms"):
        val = row.get(col, "")
        if isinstance(val, str) and val.strip():
            parts.append(val.strip())
    return " ".join(parts).lower()


def passes_screening(text_corpus: str) -> bool:
    """
    Return True if the paper passes inclusion/exclusion screening.

    Inclusion: text_corpus matches at least one localization/navigation term.
    Exclusion: if the paper matches ONLY communication/networking/signal terms
               and none of the inclusion terms, it is excluded.
    """
    if not text_corpus:
        return False

    # Check if any inclusion term matches
    has_inclusion = any(
        re.search(pattern, text_corpus, re.IGNORECASE)
        for pattern in INCLUSION_TERMS
    )

    if has_inclusion:
        return True

    # If no inclusion term, exclude entirely
    return False


def main():
    """Run the full data-cleaning pipeline."""
    print("=" * 72)
    print("  01_clean_data.py — GNSS-Denied Drone SLR Data Cleaning Pipeline")
    print("=" * 72)

    # ── 1. Load raw data ───────────────────────────────────────────────────
    print(f"\n[1/9] Loading raw CSV: {RAW_CSV}")
    if not RAW_CSV.exists():
        print(f"  ERROR: File not found → {RAW_CSV}")
        sys.exit(1)
    df = load_csv(RAW_CSV)
    total_loaded = len(df)
    print(f"  Total papers loaded: {total_loaded}")
    print(f"  Columns ({len(df.columns)}): {list(df.columns)}")

    # ── 2. Rename columns ─────────────────────────────────────────────────
    print("\n[2/9] Renaming columns...")
    df.rename(columns=COLUMN_MAP, inplace=True)
    # Keep only renamed + any extras
    kept_cols = [c for c in COLUMN_MAP.values() if c in df.columns]
    extra_cols = [c for c in df.columns if c not in COLUMN_MAP.values()]
    print(f"  Mapped columns: {kept_cols}")
    if extra_cols:
        print(f"  Extra columns (kept): {extra_cols}")

    # ── 3. Clean text fields ──────────────────────────────────────────────
    print("\n[3/9] Cleaning text fields...")
    text_columns = ["title", "abstract", "authors", "affiliations", "publication",
                    "author_keywords", "ieee_terms", "funding", "mesh_terms"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    print("  ✓ HTML tags removed, whitespace normalized")

    # ── 4. Parse year and filter ──────────────────────────────────────────
    print("\n[4/9] Parsing year and filtering (2015–2026)...")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    before_year = len(df)
    df = df[(df["year"] >= 2015) & (df["year"] <= 2026)].copy()
    after_year = len(df)
    dropped_year = before_year - after_year
    print(f"  Papers after year filter: {after_year}  (dropped {dropped_year})")
    print(f"  Year range: {int(df['year'].min())}–{int(df['year'].max())}")

    # ── 5. Parse numeric fields ───────────────────────────────────────────
    print("\n[5/9] Parsing numeric fields...")
    df["citation_count"] = pd.to_numeric(df["citation_count"], errors="coerce").fillna(0).astype(int)
    df["reference_count"] = pd.to_numeric(df.get("reference_count", 0), errors="coerce").fillna(0).astype(int)
    print(f"  ✓ citation_count: mean={df['citation_count'].mean():.1f}, "
          f"median={df['citation_count'].median():.0f}, max={df['citation_count'].max()}")

    # ── 6. Remove duplicates ──────────────────────────────────────────────
    print("\n[6/9] Removing duplicates...")
    before_dedup = len(df)

    # 6a. By DOI (keep first, ignore empty DOIs)
    doi_mask = df["doi"].notna() & (df["doi"].str.strip() != "")
    doi_dupes = df[doi_mask].duplicated(subset=["doi"], keep="first")
    n_doi_dupes = doi_dupes.sum()
    df = df[~(doi_mask & doi_dupes)].copy()
    print(f"  Duplicates by DOI: {n_doi_dupes}")

    # 6b. By exact title match (case-insensitive)
    df["_title_lower"] = df["title"].str.lower().str.strip()
    title_dupes = df.duplicated(subset=["_title_lower"], keep="first")
    n_title_dupes = title_dupes.sum()
    df = df[~title_dupes].copy()
    df.drop(columns=["_title_lower"], inplace=True)
    print(f"  Duplicates by title: {n_title_dupes}")

    after_dedup = len(df)
    print(f"  Papers after deduplication: {after_dedup}  (removed {before_dedup - after_dedup} total)")

    # ── 7. Drop rows with empty title or abstract ─────────────────────────
    print("\n[7/9] Dropping rows with empty title or abstract...")
    before_drop = len(df)
    df = df[
        (df["title"].str.strip() != "") & (df["title"].notna()) &
        (df["abstract"].str.strip() != "") & (df["abstract"].notna())
    ].copy()
    after_drop = len(df)
    dropped_empty = before_drop - after_drop
    print(f"  Dropped {dropped_empty} papers with missing title/abstract")
    print(f"  Papers remaining: {after_drop}")

    # ── 8. Build text_corpus ──────────────────────────────────────────────
    print("\n[8/9] Building text corpus and applying screening filter...")
    df["text_corpus"] = df.apply(build_text_corpus, axis=1)

    before_screen = len(df)
    df["_passes_screen"] = df["text_corpus"].apply(passes_screening)
    n_excluded = (~df["_passes_screen"]).sum()
    df = df[df["_passes_screen"]].copy()
    df.drop(columns=["_passes_screen"], inplace=True)
    after_screen = len(df)
    print(f"  Papers excluded by screening: {n_excluded}")
    print(f"  Papers after screening: {after_screen}")

    # ── 9. Reset index ────────────────────────────────────────────────────
    df.reset_index(drop=True, inplace=True)
    final_count = len(df)

    # ── 10. Print statistics ──────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("  CLEANING SUMMARY")
    print("=" * 72)

    stats_lines = []

    def log(msg):
        print(msg)
        stats_lines.append(msg)

    log(f"  Total papers loaded:              {total_loaded}")
    log(f"  Papers after year filter:         {after_year}")
    log(f"  Duplicates removed (by DOI):      {n_doi_dupes}")
    log(f"  Duplicates removed (by title):    {n_title_dupes}")
    log(f"  Papers dropped (no title/abs):    {dropped_empty}")
    log(f"  Papers excluded by screening:     {n_excluded}")
    log(f"  ─────────────────────────────────────────────")
    log(f"  FINAL paper count:                {final_count}")
    log(f"  Year range:                       {int(df['year'].min())}–{int(df['year'].max())}")

    log(f"\n  Top 10 Publication Venues:")
    top_venues = df["publication"].value_counts().head(10)
    for i, (venue, count) in enumerate(top_venues.items(), 1):
        log(f"    {i:>2}. {venue[:65]:<65s}  ({count})")

    log(f"\n  Missing Values Per Column:")
    for col in df.columns:
        if col == "text_corpus":
            continue
        n_missing = df[col].isna().sum() + (df[col].astype(str).str.strip() == "").sum()
        if n_missing > 0:
            log(f"    {col:<25s}  {n_missing:>5d}  ({100*n_missing/final_count:.1f}%)")

    # ── 11. Print sample rows ─────────────────────────────────────────────
    print(f"\n  10 Random Sample Papers:")
    print("  " + "-" * 100)
    sample = df.sample(n=min(10, len(df)), random_state=42)
    for _, row in sample.iterrows():
        title_short = row["title"][:80] + ("..." if len(row["title"]) > 80 else "")
        print(f"  [{int(row['year'])}] {title_short}")
        print(f"         DOI: {row.get('doi', 'N/A')}")
    print("  " + "-" * 100)

    # ── 12. Save cleaned data ─────────────────────────────────────────────
    output_csv = PROCESSED_DIR / "database_final.csv"
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"\n  ✓ Saved cleaned data → {output_csv}")
    print(f"    Rows: {len(df)}, Columns: {len(df.columns)}")

    # ── 13. Save summary report ───────────────────────────────────────────
    report_path = OUTPUT_DIR / "checkpoint1_summary.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("CHECKPOINT 1 — Data Cleaning Summary\n")
        f.write("=" * 60 + "\n")
        f.write(f"Date: 2026-07-12\n")
        f.write(f"Raw CSV: {RAW_CSV.name}\n")
        f.write(f"Output: {output_csv.name}\n\n")
        for line in stats_lines:
            f.write(line.strip() + "\n")
        f.write(f"\nColumns in final dataset:\n")
        for col in df.columns:
            f.write(f"  - {col}\n")
        f.write(f"\nYear distribution:\n")
        year_dist = df["year"].value_counts().sort_index()
        for yr, cnt in year_dist.items():
            f.write(f"  {int(yr)}: {cnt}\n")
    print(f"  ✓ Saved summary report → {report_path}")

    print("\n" + "=" * 72)
    print("  Pipeline Stage 1 COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
