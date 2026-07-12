#!/usr/bin/env python3
"""
03_generate_figures.py
======================
Generate publication-quality figures and summary tables for the
GNSS-Denied Drone Localization Systematic Literature Review.

Reads  : data/processed/classified_papers.csv
Writes : analysis/output/figures/fig01..fig10_*.png
         analysis/output/tables.md

All figures follow IEEE publication standards:
  - White background, high contrast
  - 300 DPI PNG
  - Professional serif/sans-serif typography
  - Consistent curated colour palette

Author : SLR Pipeline
Date   : 2026-07-12
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path
from collections import Counter
from itertools import product as iter_product

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Fix Windows console encoding for Unicode output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Resolve project root ────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "classified_papers.csv"
FIGURES_DIR = BASE_DIR / "analysis" / "output" / "figures"
TABLES_PATH = BASE_DIR / "analysis" / "output" / "tables.md"

# ── Colour palette (12 high-contrast, IEEE-friendly) ───────────────
COLORS = [
    "#2E86AB",  # Steel Blue
    "#A23B72",  # Plum
    "#F18F01",  # Orange
    "#C73E1D",  # Vermilion
    "#3B1F2B",  # Dark Aubergine
    "#44BBA4",  # Teal
    "#E94F37",  # Tomato Red
    "#393E41",  # Charcoal
    "#D4A373",  # Tan
    "#6A994E",  # Olive Green
    "#BC4749",  # Brick Red
    "#5C6B73",  # Slate Grey
]

# ── Matplotlib global styling ──────────────────────────────────────
def setup_matplotlib():
    """Configure matplotlib for IEEE-standard figures."""
    plt.rcdefaults()
    # Try serif font stack; fall back to sans-serif
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
    print("[✓] Matplotlib configured for IEEE-standard output.")


# ── Helper utilities ───────────────────────────────────────────────
def explode_column(df: pd.DataFrame, col: str) -> pd.Series:
    """Split a semicolon-separated column and return a flat Series of values."""
    values = (
        df[col]
        .dropna()
        .str.split(r"\s*;\s*")
        .explode()
        .str.strip()
    )
    # Remove empty strings
    values = values[values.astype(bool)]
    return values


def save_figure(fig: plt.Figure, name: str) -> Path:
    """Save figure and return path."""
    path = FIGURES_DIR / name
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → Saved: {path.relative_to(BASE_DIR)}")
    return path


def add_bar_labels(ax, fmt: str = "{:.0f}", fontsize: int = 9,
                   orientation: str = "vertical"):
    """Add value labels to bars."""
    for container in ax.containers:
        if orientation == "vertical":
            ax.bar_label(container, fmt=fmt, fontsize=fontsize,
                         padding=3, color="#333333")
        else:
            ax.bar_label(container, fmt=fmt, fontsize=fontsize,
                         padding=3, color="#333333")


# ═══════════════════════════════════════════════════════════════════
# Figure generation functions
# ═══════════════════════════════════════════════════════════════════

def fig01_papers_per_year(df: pd.DataFrame) -> Path:
    """Bar chart – papers published per year."""
    print("\n[Fig 01] Papers per year …")
    year_counts = df["year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(year_counts.index.astype(str), year_counts.values,
                  color=COLORS[0], edgecolor="white", linewidth=0.5)
    add_bar_labels(ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    ax.set_title("Distribution of Publications by Year", fontweight="bold")
    fig.tight_layout()
    return save_figure(fig, "fig01_papers_per_year.png")


def fig02_sensor_usage(df: pd.DataFrame) -> Path:
    """Horizontal bar chart – sensor modality frequency."""
    print("\n[Fig 02] Sensor usage …")
    sensors = explode_column(df, "sensors")
    counts = sensors.value_counts()
    counts = counts[counts > 0]

    fig, ax = plt.subplots(figsize=(10, max(6, len(counts) * 0.35)))
    y_pos = range(len(counts))
    ax.barh(y_pos, counts.values, color=[COLORS[i % len(COLORS)]
            for i in range(len(counts))], edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(counts.index)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Papers")
    ax.set_title("Sensor Modality Usage in GNSS-Denied Localization Studies",
                 fontweight="bold")
    # Add value labels
    for i, v in enumerate(counts.values):
        ax.text(v + 0.3, i, str(v), va="center", fontsize=9, color="#333333")
    fig.tight_layout()
    return save_figure(fig, "fig02_sensor_usage.png")


def fig03_algorithm_usage(df: pd.DataFrame) -> Path:
    """Horizontal bar chart – algorithm/framework frequency."""
    print("\n[Fig 03] Algorithm usage …")
    algos = explode_column(df, "algorithms")
    counts = algos.value_counts()
    counts = counts[counts > 0]

    fig, ax = plt.subplots(figsize=(10, max(6, len(counts) * 0.35)))
    y_pos = range(len(counts))
    ax.barh(y_pos, counts.values, color=[COLORS[i % len(COLORS)]
            for i in range(len(counts))], edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(counts.index)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Papers")
    ax.set_title("Algorithm/Framework Usage Frequency", fontweight="bold")
    for i, v in enumerate(counts.values):
        ax.text(v + 0.3, i, str(v), va="center", fontsize=9, color="#333333")
    fig.tight_layout()
    return save_figure(fig, "fig03_algorithm_usage.png")


def fig04_application_domains(df: pd.DataFrame) -> Path:
    """Horizontal bar chart – application domains."""
    print("\n[Fig 04] Application domains …")
    apps = explode_column(df, "applications")
    counts = apps.value_counts()
    counts = counts[counts > 0]

    fig, ax = plt.subplots(figsize=(10, max(6, len(counts) * 0.4)))
    y_pos = range(len(counts))
    ax.barh(y_pos, counts.values, color=[COLORS[i % len(COLORS)]
            for i in range(len(counts))], edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(counts.index)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Papers")
    ax.set_title("Application Domain Distribution", fontweight="bold")
    for i, v in enumerate(counts.values):
        ax.text(v + 0.3, i, str(v), va="center", fontsize=9, color="#333333")
    fig.tight_layout()
    return save_figure(fig, "fig04_application_domains.png")


def fig05_sensor_algorithm_heatmap(df: pd.DataFrame) -> Path:
    """Heatmap – sensor × algorithm co-occurrence matrix."""
    print("\n[Fig 05] Sensor–Algorithm heatmap …")

    # Build co-occurrence pairs
    pairs: list[tuple[str, str]] = []
    for _, row in df.iterrows():
        if pd.isna(row.get("sensors")) or pd.isna(row.get("algorithms")):
            continue
        s_list = [s.strip() for s in str(row["sensors"]).split(";") if s.strip()]
        a_list = [a.strip() for a in str(row["algorithms"]).split(";") if a.strip()]
        for s, a in iter_product(s_list, a_list):
            pairs.append((s, a))

    if not pairs:
        print("  ⚠ No co-occurrence data — skipping heatmap.")
        return None

    pair_df = pd.DataFrame(pairs, columns=["Sensor", "Algorithm"])
    co_matrix = pair_df.groupby(["Sensor", "Algorithm"]).size().unstack(fill_value=0)

    # Select top N
    top_sensors = co_matrix.sum(axis=1).nlargest(15).index
    top_algos = co_matrix.sum(axis=0).nlargest(12).index
    co_sub = co_matrix.loc[
        co_matrix.index.isin(top_sensors),
        co_matrix.columns.isin(top_algos),
    ]

    fig, ax = plt.subplots(figsize=(14, 9))
    sns.heatmap(
        co_sub, annot=True, fmt="d", cmap="YlOrRd",
        linewidths=0.5, linecolor="white",
        cbar_kws={"label": "Co-occurrence Count"},
        ax=ax,
    )
    ax.set_title("Sensor–Algorithm Co-occurrence Matrix", fontweight="bold")
    ax.set_xlabel("Algorithm / Framework")
    ax.set_ylabel("Sensor Modality")
    plt.xticks(rotation=40, ha="right")
    plt.yticks(rotation=0)
    fig.tight_layout()
    return save_figure(fig, "fig05_sensor_algorithm_heatmap.png")


def fig06_temporal_trends_sensors(df: pd.DataFrame) -> Path:
    """Grouped bar chart – top 6 sensors over time."""
    print("\n[Fig 06] Temporal trends – sensors …")

    # Explode sensors with year
    rows = []
    for _, r in df.iterrows():
        if pd.isna(r.get("sensors")) or pd.isna(r.get("year")):
            continue
        for s in str(r["sensors"]).split(";"):
            s = s.strip()
            if s:
                rows.append({"year": int(r["year"]), "sensor": s})
    if not rows:
        print("  ⚠ No sensor-year data — skipping.")
        return None

    tmp = pd.DataFrame(rows)
    top6 = tmp["sensor"].value_counts().head(6).index.tolist()
    tmp = tmp[tmp["sensor"].isin(top6)]
    pivot = tmp.groupby(["year", "sensor"]).size().unstack(fill_value=0)
    # Reindex to have all top6 columns
    for s in top6:
        if s not in pivot.columns:
            pivot[s] = 0
    pivot = pivot[top6]

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(pivot.index))
    width = 0.13
    for i, sensor in enumerate(top6):
        offset = (i - len(top6) / 2 + 0.5) * width
        ax.bar(x + offset, pivot[sensor].values, width,
               label=sensor, color=COLORS[i % len(COLORS)],
               edgecolor="white", linewidth=0.3)
    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index.astype(int))
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    ax.set_title("Evolution of Sensor Usage Over Time", fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9, edgecolor="#cccccc")
    fig.tight_layout()
    return save_figure(fig, "fig06_temporal_trends_sensors.png")


def fig07_temporal_trends_algorithms(df: pd.DataFrame) -> Path:
    """Line chart – top 6 algorithms over time."""
    print("\n[Fig 07] Temporal trends – algorithms …")

    rows = []
    for _, r in df.iterrows():
        if pd.isna(r.get("algorithms")) or pd.isna(r.get("year")):
            continue
        for a in str(r["algorithms"]).split(";"):
            a = a.strip()
            if a:
                rows.append({"year": int(r["year"]), "algorithm": a})
    if not rows:
        print("  ⚠ No algorithm-year data — skipping.")
        return None

    tmp = pd.DataFrame(rows)
    top6 = tmp["algorithm"].value_counts().head(6).index.tolist()
    tmp = tmp[tmp["algorithm"].isin(top6)]
    pivot = tmp.groupby(["year", "algorithm"]).size().unstack(fill_value=0)
    for a in top6:
        if a not in pivot.columns:
            pivot[a] = 0
    pivot = pivot[top6]

    markers = ["o", "s", "D", "^", "v", "P"]
    linestyles = ["-", "--", "-.", ":", "-", "--"]

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, algo in enumerate(top6):
        ax.plot(
            pivot.index, pivot[algo].values,
            marker=markers[i % len(markers)],
            linestyle=linestyles[i % len(linestyles)],
            color=COLORS[i % len(COLORS)],
            linewidth=2, markersize=7, label=algo,
        )
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    ax.set_title("Algorithm Adoption Trends (2019–2025)", fontweight="bold")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.legend(loc="upper left", framealpha=0.9, edgecolor="#cccccc")
    fig.tight_layout()
    return save_figure(fig, "fig07_temporal_trends_algorithms.png")


def fig08_environment_distribution(df: pd.DataFrame) -> Path:
    """Bar chart – evaluation environment distribution."""
    print("\n[Fig 08] Environment distribution …")
    envs = explode_column(df, "environments")
    counts = envs.value_counts()
    counts = counts[counts > 0]

    if counts.empty:
        print("  ⚠ No environment data — skipping.")
        return None

    fig, ax = plt.subplots(figsize=(10, max(6, len(counts) * 0.4)))
    y_pos = range(len(counts))
    ax.barh(y_pos, counts.values, color=[COLORS[i % len(COLORS)]
            for i in range(len(counts))], edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(counts.index)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Papers")
    ax.set_title("Evaluation Environment Distribution", fontweight="bold")
    for i, v in enumerate(counts.values):
        ax.text(v + 0.3, i, str(v), va="center", fontsize=9, color="#333333")
    fig.tight_layout()
    return save_figure(fig, "fig08_environment_distribution.png")


def fig09_top_venues(df: pd.DataFrame) -> Path:
    """Horizontal bar chart – top 15 publication venues."""
    print("\n[Fig 09] Top venues …")
    venue_counts = (
        df["publication"]
        .dropna()
        .str.strip()
        .value_counts()
        .head(15)
    )
    if venue_counts.empty:
        print("  ⚠ No publication venue data — skipping.")
        return None

    fig, ax = plt.subplots(figsize=(12, 8))
    y_pos = range(len(venue_counts))
    ax.barh(y_pos, venue_counts.values, color=[COLORS[i % len(COLORS)]
            for i in range(len(venue_counts))], edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(venue_counts.index, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Papers")
    ax.set_title("Top 15 Publication Venues", fontweight="bold")
    for i, v in enumerate(venue_counts.values):
        ax.text(v + 0.15, i, str(v), va="center", fontsize=9, color="#333333")
    fig.tight_layout()
    return save_figure(fig, "fig09_top_venues.png")


def fig10_top_datasets(df: pd.DataFrame) -> Path:
    """Horizontal bar chart – benchmark datasets used."""
    print("\n[Fig 10] Top datasets …")
    if "datasets" not in df.columns:
        print("  ⚠ 'datasets' column not found — skipping.")
        return None

    datasets = explode_column(df, "datasets")
    # Exclude common "none" / "not specified" markers
    exclude = {"", "nan", "none", "n/a", "not specified", "not available",
               "unspecified", "custom", "proprietary", "-"}
    datasets = datasets[~datasets.str.lower().isin(exclude)]
    counts = datasets.value_counts()
    if counts.empty:
        print("  ⚠ No dataset data after filtering — skipping.")
        return None

    top = counts.head(20)
    fig, ax = plt.subplots(figsize=(10, max(6, len(top) * 0.4)))
    y_pos = range(len(top))
    ax.barh(y_pos, top.values, color=[COLORS[i % len(COLORS)]
            for i in range(len(top))], edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top.index, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Papers")
    ax.set_title("Benchmark Datasets Used", fontweight="bold")
    for i, v in enumerate(top.values):
        ax.text(v + 0.15, i, str(v), va="center", fontsize=9, color="#333333")
    fig.tight_layout()
    return save_figure(fig, "fig10_top_datasets.png")


# ═══════════════════════════════════════════════════════════════════
# Markdown tables generation
# ═══════════════════════════════════════════════════════════════════

def generate_tables(df: pd.DataFrame) -> str:
    """Return a Markdown string with five summary tables."""
    md_parts: list[str] = []

    # ── Table 1: Summary Statistics ─────────────────────────────────
    md_parts.append("# Summary Tables — GNSS-Denied Localization SLR\n")
    md_parts.append("## Table 1: Summary Statistics\n")
    sensors_all = explode_column(df, "sensors") if "sensors" in df.columns else pd.Series(dtype=str)
    algos_all = explode_column(df, "algorithms") if "algorithms" in df.columns else pd.Series(dtype=str)
    apps_all = explode_column(df, "applications") if "applications" in df.columns else pd.Series(dtype=str)
    datasets_all = explode_column(df, "datasets") if "datasets" in df.columns else pd.Series(dtype=str)

    stats = {
        "Total papers": len(df),
        "Year range": f"{int(df['year'].min())}–{int(df['year'].max())}" if "year" in df.columns else "N/A",
        "Unique publication venues": df["publication"].nunique() if "publication" in df.columns else "N/A",
        "Unique sensor modalities": sensors_all.nunique(),
        "Unique algorithms/frameworks": algos_all.nunique(),
        "Unique application domains": apps_all.nunique(),
        "Unique datasets": datasets_all.nunique(),
        "Median citation count": df["citation_count"].median() if "citation_count" in df.columns else "N/A",
        "Mean citation count": f"{df['citation_count'].mean():.1f}" if "citation_count" in df.columns else "N/A",
    }
    md_parts.append("| Metric | Value |")
    md_parts.append("|--------|------:|")
    for k, v in stats.items():
        md_parts.append(f"| {k} | {v} |")
    md_parts.append("")

    # ── Table 2: Top 20 Sensor–Algorithm Combinations ───────────────
    md_parts.append("## Table 2: Top 20 Sensor–Algorithm Combinations\n")
    pairs: list[tuple[str, str]] = []
    for _, row in df.iterrows():
        if pd.isna(row.get("sensors")) or pd.isna(row.get("algorithms")):
            continue
        s_list = [s.strip() for s in str(row["sensors"]).split(";") if s.strip()]
        a_list = [a.strip() for a in str(row["algorithms"]).split(";") if a.strip()]
        for s, a in iter_product(s_list, a_list):
            pairs.append((s, a))
    if pairs:
        combo_counts = Counter(pairs).most_common(20)
        md_parts.append("| Rank | Sensor | Algorithm | Count |")
        md_parts.append("|-----:|--------|-----------|------:|")
        for i, ((s, a), c) in enumerate(combo_counts, 1):
            md_parts.append(f"| {i} | {s} | {a} | {c} |")
    else:
        md_parts.append("_No data available._")
    md_parts.append("")

    # ── Table 3: Top 15 Publication Venues ──────────────────────────
    md_parts.append("## Table 3: Top 15 Publication Venues\n")
    if "publication" in df.columns:
        venue_counts = df["publication"].dropna().str.strip().value_counts().head(15)
        md_parts.append("| Rank | Venue | Papers |")
        md_parts.append("|-----:|-------|-------:|")
        for i, (venue, cnt) in enumerate(venue_counts.items(), 1):
            md_parts.append(f"| {i} | {venue} | {cnt} |")
    else:
        md_parts.append("_No data available._")
    md_parts.append("")

    # ── Table 4: Dataset Usage Summary ──────────────────────────────
    md_parts.append("## Table 4: Dataset Usage Summary\n")
    if "datasets" in df.columns:
        ds = explode_column(df, "datasets")
        exclude = {"", "nan", "none", "n/a", "not specified", "not available",
                   "unspecified", "custom", "proprietary", "-"}
        ds = ds[~ds.str.lower().isin(exclude)]
        ds_counts = ds.value_counts()
        if not ds_counts.empty:
            md_parts.append("| Dataset | Papers |")
            md_parts.append("|---------|-------:|")
            for ds_name, cnt in ds_counts.items():
                md_parts.append(f"| {ds_name} | {cnt} |")
        else:
            md_parts.append("_No named datasets found after filtering._")
    else:
        md_parts.append("_'datasets' column not found._")
    md_parts.append("")

    # ── Table 5: Sensor Usage per Application Domain ────────────────
    md_parts.append("## Table 5: Sensor Usage per Application Domain (Cross-tabulation)\n")
    if "sensors" in df.columns and "applications" in df.columns:
        cross_rows = []
        for _, row in df.iterrows():
            if pd.isna(row.get("sensors")) or pd.isna(row.get("applications")):
                continue
            s_list = [s.strip() for s in str(row["sensors"]).split(";") if s.strip()]
            a_list = [a.strip() for a in str(row["applications"]).split(";") if a.strip()]
            for s, a in iter_product(s_list, a_list):
                cross_rows.append({"sensor": s, "application": a})
        if cross_rows:
            cross_df = pd.DataFrame(cross_rows)
            ct = cross_df.groupby(["application", "sensor"]).size().unstack(fill_value=0)
            # Keep top 10 sensors to keep table readable
            top_sensors = cross_df["sensor"].value_counts().head(10).index.tolist()
            ct = ct[[s for s in top_sensors if s in ct.columns]]
            header = "| Application | " + " | ".join(ct.columns) + " |"
            sep = "|-------------|" + "|".join(["------:" for _ in ct.columns]) + "|"
            md_parts.append(header)
            md_parts.append(sep)
            for app, vals in ct.iterrows():
                row_str = " | ".join(str(v) for v in vals.values)
                md_parts.append(f"| {app} | {row_str} |")
        else:
            md_parts.append("_No data available._")
    else:
        md_parts.append("_Required columns not found._")
    md_parts.append("")

    return "\n".join(md_parts)


# ═══════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("  GNSS-Denied Drone SLR — Figure & Table Generation Pipeline")
    print("=" * 65)

    # ── Load data ───────────────────────────────────────────────────
    if not DATA_PATH.exists():
        sys.exit(f"[✗] Data file not found: {DATA_PATH}")

    print(f"\n[•] Loading data from {DATA_PATH.relative_to(BASE_DIR)} …")
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    print(f"    Loaded {len(df)} papers  |  Columns: {list(df.columns)}")

    # ── Setup ───────────────────────────────────────────────────────
    setup_matplotlib()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_PATH.parent.mkdir(parents=True, exist_ok=True)

    # ── Generate figures ────────────────────────────────────────────
    generated: list[str] = []

    figure_funcs = [
        ("fig01", fig01_papers_per_year),
        ("fig02", fig02_sensor_usage),
        ("fig03", fig03_algorithm_usage),
        ("fig04", fig04_application_domains),
        ("fig05", fig05_sensor_algorithm_heatmap),
        ("fig06", fig06_temporal_trends_sensors),
        ("fig07", fig07_temporal_trends_algorithms),
        ("fig08", fig08_environment_distribution),
        ("fig09", fig09_top_venues),
        ("fig10", fig10_top_datasets),
    ]

    for tag, func in figure_funcs:
        try:
            path = func(df)
            if path:
                generated.append(tag)
        except Exception as exc:
            print(f"  ✗ {tag} failed: {exc}")

    # ── Generate tables ─────────────────────────────────────────────
    print("\n[•] Generating summary tables …")
    tables_md = generate_tables(df)
    TABLES_PATH.write_text(tables_md, encoding="utf-8")
    print(f"  → Saved: {TABLES_PATH.relative_to(BASE_DIR)}")

    # ── Final summary ──────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  Summary")
    print("=" * 65)
    print(f"  Total figures generated : {len(generated)} / 10")
    print(f"  Figures                 : {', '.join(generated)}")
    print(f"  Tables file             : {TABLES_PATH.relative_to(BASE_DIR)}")
    print(f"  Output directory        : {FIGURES_DIR.relative_to(BASE_DIR)}")
    print("=" * 65)


if __name__ == "__main__":
    main()
