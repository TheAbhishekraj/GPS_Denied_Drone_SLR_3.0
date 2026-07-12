#!/usr/bin/env python3
"""
04_extract_accuracy.py
======================
Extract quantitative accuracy / error metrics from paper abstracts
(and text_corpus if available) using regex pattern matching.

Reads  : data/processed/classified_papers.csv
Writes : data/processed/accuracy_data.csv
         analysis/output/figures/fig11_accuracy_by_sensor.png   (if >= 10 pts)
         analysis/output/figures/fig12_accuracy_by_algorithm.png (if >= 10 pts)
         analysis/output/checkpoint3_accuracy_summary.txt

Author : SLR Pipeline
Date   : 2026-07-12
"""

from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Fix Windows console encoding for Unicode output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Resolve project root ────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "classified_papers.csv"
OUTPUT_CSV = BASE_DIR / "data" / "processed" / "accuracy_data.csv"
FIGURES_DIR = BASE_DIR / "analysis" / "output" / "figures"
SUMMARY_PATH = BASE_DIR / "analysis" / "output" / "checkpoint3_accuracy_summary.txt"

# ── Colour palette ──────────────────────────────────────────────────
COLORS = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B",
    "#44BBA4", "#E94F37", "#393E41", "#D4A373", "#6A994E",
    "#BC4749", "#5C6B73",
]

# ── Regex patterns for accuracy extraction ──────────────────────────
PATTERNS_METRIC = [
    # Pattern 1: Metric name → value unit
    re.compile(
        r"(?i)(?:ATE|RMSE|RMS|root mean square error|position error|"
        r"trajectory error|localization error|translation error|drift|"
        r"mean error|average error|absolute error)"
        r"\s*(?:of|is|was|:=|=)?\s*"
        r"(?:about|approximately|around|less than|under|within)?\s*"
        r"(\d+\.?\d*)\s*"
        r"(m|cm|mm|meter|meters|centimeter|centimeters|millimeter|millimeters)\b"
    ),
    # Pattern 2: Value unit → metric name
    re.compile(
        r"(?i)(\d+\.?\d*)\s*(?:-)?\s*"
        r"(m|cm|mm)\s+"
        r"(?:RMSE|ATE|error|accuracy|precision|position error)"
    ),
    # Pattern 3: accuracy/error of X unit
    re.compile(
        r"(?i)(?:accuracy|error|precision)\s+"
        r"(?:of|around|about|approximately)?\s*"
        r"(\d+\.?\d*)\s*(m|cm|mm)"
    ),
]

PATTERN_PERCENT = re.compile(
    r"(?i)(?:drift|error|accuracy)\s*"
    r"(?:of|is|was|:=|=)?\s*"
    r"(?:about|approximately|less than)?\s*"
    r"(\d+\.?\d*)\s*(%|percent)"
)

# ── Unit normalisation ──────────────────────────────────────────────
UNIT_TO_METRES: dict[str, float] = {
    "m": 1.0, "meter": 1.0, "meters": 1.0,
    "cm": 0.01, "centimeter": 0.01, "centimeters": 0.01,
    "mm": 0.001, "millimeter": 0.001, "millimeters": 0.001,
}


def setup_matplotlib():
    """IEEE-standard matplotlib config."""
    plt.rcdefaults()
    try:
        matplotlib.rcParams["font.family"] = "serif"
        matplotlib.rcParams["font.serif"] = [
            "Times New Roman", "DejaVu Serif", "Georgia", "serif"
        ]
    except Exception:
        matplotlib.rcParams["font.family"] = "sans-serif"

    matplotlib.rcParams.update({
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#222222",
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "text.color": "#222222",
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    warnings.filterwarnings("ignore", category=UserWarning)


# ── Core extraction logic ───────────────────────────────────────────

def extract_accuracy_from_text(text: str) -> list[dict]:
    """
    Return a list of dicts with keys:
        value_m        – float, accuracy converted to metres
        unit_original  – str,  original unit string
        text_match     – str,  matched snippet
        is_percent     – bool
    """
    if not isinstance(text, str) or not text.strip():
        return []

    results: list[dict] = []

    # Metric patterns (distance-based)
    for pat in PATTERNS_METRIC:
        for m in pat.finditer(text):
            val_str, unit = m.group(1), m.group(2).lower()
            try:
                val = float(val_str)
            except ValueError:
                continue
            if val <= 0:
                continue
            factor = UNIT_TO_METRES.get(unit, 1.0)
            results.append({
                "value_m": val * factor,
                "unit_original": unit,
                "text_match": m.group(0).strip(),
                "is_percent": False,
            })

    # Percentage pattern
    for m in PATTERN_PERCENT.finditer(text):
        val_str = m.group(1)
        try:
            val = float(val_str)
        except ValueError:
            continue
        if val <= 0:
            continue
        results.append({
            "value_m": val,  # stored as-is, flagged as %
            "unit_original": "%",
            "text_match": m.group(0).strip(),
            "is_percent": True,
        })

    return results


def pick_best_match(matches: list[dict]) -> dict | None:
    """
    Among distance-based matches, return the smallest non-zero value.
    If only percentage matches exist, return the smallest of those.
    """
    distance = [m for m in matches if not m["is_percent"]]
    pct = [m for m in matches if m["is_percent"]]

    if distance:
        return min(distance, key=lambda m: m["value_m"])
    if pct:
        return min(pct, key=lambda m: m["value_m"])
    return None


# ── Main pipeline ───────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  GNSS-Denied Drone SLR — Accuracy Extraction Pipeline")
    print("=" * 65)

    # ── Load ────────────────────────────────────────────────────────
    if not DATA_PATH.exists():
        sys.exit(f"[✗] Data file not found: {DATA_PATH}")

    print(f"\n[•] Loading {DATA_PATH.relative_to(BASE_DIR)} …")
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    print(f"    Loaded {len(df)} papers.")

    # Decide which text fields to search
    text_cols = ["abstract"]
    if "text_corpus" in df.columns:
        text_cols.append("text_corpus")
        print(f"    Will search columns: {text_cols}")
    else:
        print("    'text_corpus' column not found — searching 'abstract' only.")

    # ── Extract ─────────────────────────────────────────────────────
    print("\n[•] Extracting accuracy metrics …")
    records: list[dict] = []
    papers_with_match = 0

    for idx, row in df.iterrows():
        # Combine text fields
        combined_text = " ".join(
            str(row[c]) for c in text_cols if pd.notna(row.get(c))
        )
        matches = extract_accuracy_from_text(combined_text)
        best = pick_best_match(matches)
        if best is None:
            continue

        papers_with_match += 1
        records.append({
            "doi": row.get("doi", ""),
            "title": row.get("title", ""),
            "year": row.get("year", ""),
            "sensors": row.get("sensors", ""),
            "algorithms": row.get("algorithms", ""),
            "applications": row.get("applications", ""),
            "environments": row.get("environments", ""),
            "accuracy_m": best["value_m"] if not best["is_percent"] else np.nan,
            "accuracy_pct": best["value_m"] if best["is_percent"] else np.nan,
            "accuracy_unit_original": best["unit_original"],
            "accuracy_text_match": best["text_match"],
        })

    acc_df = pd.DataFrame(records)
    print(f"    Papers with extractable accuracy: {papers_with_match} / {len(df)}"
          f" ({papers_with_match/len(df)*100:.1f}%)")

    # ── Save CSV ────────────────────────────────────────────────────
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    acc_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"    → Saved: {OUTPUT_CSV.relative_to(BASE_DIR)}")

    # ── Statistics ──────────────────────────────────────────────────
    summary_lines: list[str] = []
    summary_lines.append("=" * 65)
    summary_lines.append("  Accuracy Extraction Summary")
    summary_lines.append("=" * 65)
    summary_lines.append(f"Total papers analysed       : {len(df)}")
    summary_lines.append(f"Papers with accuracy data   : {papers_with_match}"
                         f" ({papers_with_match/len(df)*100:.1f}%)")

    dist_df = acc_df.dropna(subset=["accuracy_m"])
    if not dist_df.empty:
        summary_lines.append(f"\nDistance-based accuracy (metres):")
        summary_lines.append(f"  Count  : {len(dist_df)}")
        summary_lines.append(f"  Min    : {dist_df['accuracy_m'].min():.4f} m")
        summary_lines.append(f"  Max    : {dist_df['accuracy_m'].max():.4f} m")
        summary_lines.append(f"  Median : {dist_df['accuracy_m'].median():.4f} m")
        summary_lines.append(f"  Mean   : {dist_df['accuracy_m'].mean():.4f} m")
        summary_lines.append(f"  Std    : {dist_df['accuracy_m'].std():.4f} m")

    pct_df = acc_df.dropna(subset=["accuracy_pct"])
    if not pct_df.empty:
        summary_lines.append(f"\nPercentage-based accuracy:")
        summary_lines.append(f"  Count  : {len(pct_df)}")
        summary_lines.append(f"  Min    : {pct_df['accuracy_pct'].min():.2f}%")
        summary_lines.append(f"  Max    : {pct_df['accuracy_pct'].max():.2f}%")
        summary_lines.append(f"  Median : {pct_df['accuracy_pct'].median():.2f}%")

    # Breakdown by sensor
    if not dist_df.empty and "sensors" in dist_df.columns:
        summary_lines.append("\nAccuracy by sensor type (distance, top 10):")
        sensor_rows = []
        for _, r in dist_df.iterrows():
            if pd.isna(r["sensors"]):
                continue
            for s in str(r["sensors"]).split(";"):
                s = s.strip()
                if s:
                    sensor_rows.append({"sensor": s, "accuracy_m": r["accuracy_m"]})
        if sensor_rows:
            s_df = pd.DataFrame(sensor_rows)
            sensor_stats = (
                s_df.groupby("sensor")["accuracy_m"]
                .agg(["count", "median", "mean"])
                .sort_values("count", ascending=False)
                .head(10)
            )
            for sensor, row_s in sensor_stats.iterrows():
                summary_lines.append(
                    f"  {sensor:30s}  n={int(row_s['count']):3d}  "
                    f"median={row_s['median']:.4f}m  mean={row_s['mean']:.4f}m"
                )

    # Breakdown by algorithm
    if not dist_df.empty and "algorithms" in dist_df.columns:
        summary_lines.append("\nAccuracy by algorithm type (distance, top 10):")
        algo_rows = []
        for _, r in dist_df.iterrows():
            if pd.isna(r["algorithms"]):
                continue
            for a in str(r["algorithms"]).split(";"):
                a = a.strip()
                if a:
                    algo_rows.append({"algorithm": a, "accuracy_m": r["accuracy_m"]})
        if algo_rows:
            a_df = pd.DataFrame(algo_rows)
            algo_stats = (
                a_df.groupby("algorithm")["accuracy_m"]
                .agg(["count", "median", "mean"])
                .sort_values("count", ascending=False)
                .head(10)
            )
            for algo, row_a in algo_stats.iterrows():
                summary_lines.append(
                    f"  {algo:30s}  n={int(row_a['count']):3d}  "
                    f"median={row_a['median']:.4f}m  mean={row_a['mean']:.4f}m"
                )

    summary_text = "\n".join(summary_lines)
    print(f"\n{summary_text}")

    # ── Save summary ────────────────────────────────────────────────
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(summary_text, encoding="utf-8")
    print(f"\n    → Summary saved: {SUMMARY_PATH.relative_to(BASE_DIR)}")

    # ── Optional figures (if >= 10 data points) ─────────────────────
    if len(dist_df) >= 10:
        print("\n[•] Generating accuracy figures …")
        setup_matplotlib()
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        _generate_accuracy_figures(dist_df)
    else:
        print(f"\n[•] Only {len(dist_df)} distance-based data points — "
              "skipping box-plot figures (need >= 10).")

    print("\n" + "=" * 65)
    print("  Accuracy extraction complete.")
    print("=" * 65)


def _generate_accuracy_figures(dist_df: pd.DataFrame):
    """Generate boxplots of accuracy by sensor and algorithm."""

    # ── Fig 11: Accuracy by sensor ──────────────────────────────────
    sensor_rows = []
    for _, r in dist_df.iterrows():
        if pd.isna(r.get("sensors")):
            continue
        for s in str(r["sensors"]).split(";"):
            s = s.strip()
            if s:
                sensor_rows.append({"sensor": s, "accuracy_m": r["accuracy_m"]})

    if sensor_rows:
        s_df = pd.DataFrame(sensor_rows)
        # Keep sensors with >= 3 papers for meaningful boxplots
        valid_sensors = s_df["sensor"].value_counts()
        valid_sensors = valid_sensors[valid_sensors >= 3].index.tolist()
        s_df = s_df[s_df["sensor"].isin(valid_sensors)]

        if not s_df.empty:
            # Sort by median accuracy
            order = (
                s_df.groupby("sensor")["accuracy_m"]
                .median()
                .sort_values()
                .index.tolist()
            )
            fig, ax = plt.subplots(figsize=(10, max(6, len(order) * 0.45)))
            sns.boxplot(
                data=s_df, y="sensor", x="accuracy_m", order=order,
                palette=COLORS[:len(order)], orient="h",
                flierprops={"marker": "o", "markersize": 4, "alpha": 0.5},
                ax=ax,
            )
            ax.set_xlabel("Accuracy (metres, lower is better)")
            ax.set_ylabel("Sensor Modality")
            ax.set_title("Reported Accuracy by Sensor Type", fontweight="bold")
            fig.tight_layout()
            path = FIGURES_DIR / "fig11_accuracy_by_sensor.png"
            fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
            plt.close(fig)
            print(f"  → Saved: {path.relative_to(BASE_DIR)}")

    # ── Fig 12: Accuracy by algorithm ───────────────────────────────
    algo_rows = []
    for _, r in dist_df.iterrows():
        if pd.isna(r.get("algorithms")):
            continue
        for a in str(r["algorithms"]).split(";"):
            a = a.strip()
            if a:
                algo_rows.append({"algorithm": a, "accuracy_m": r["accuracy_m"]})

    if algo_rows:
        a_df = pd.DataFrame(algo_rows)
        valid_algos = a_df["algorithm"].value_counts()
        valid_algos = valid_algos[valid_algos >= 3].index.tolist()
        a_df = a_df[a_df["algorithm"].isin(valid_algos)]

        if not a_df.empty:
            order = (
                a_df.groupby("algorithm")["accuracy_m"]
                .median()
                .sort_values()
                .index.tolist()
            )
            fig, ax = plt.subplots(figsize=(10, max(6, len(order) * 0.45)))
            sns.boxplot(
                data=a_df, y="algorithm", x="accuracy_m", order=order,
                palette=COLORS[:len(order)], orient="h",
                flierprops={"marker": "o", "markersize": 4, "alpha": 0.5},
                ax=ax,
            )
            ax.set_xlabel("Accuracy (metres, lower is better)")
            ax.set_ylabel("Algorithm / Framework")
            ax.set_title("Reported Accuracy by Algorithm Type", fontweight="bold")
            fig.tight_layout()
            path = FIGURES_DIR / "fig12_accuracy_by_algorithm.png"
            fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
            plt.close(fig)
            print(f"  → Saved: {path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
