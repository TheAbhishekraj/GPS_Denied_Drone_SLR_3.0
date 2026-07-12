#!/usr/bin/env python3
"""
06_write_report.py — Generate a detailed analysis report from classified papers.

Reads the classified papers dataset, accuracy data, and generates:
  - analysis/output/report.md — Comprehensive analysis report with all findings
  - Summarises all research question answers

Part of the GNSS-Denied Localization SLR Pipeline.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import Counter

# Fix Windows console encoding for Unicode output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "analysis" / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def explode_column(df: pd.DataFrame, col: str) -> pd.Series:
    """Explode a semicolon-separated column and count values."""
    values = df[col].dropna().str.split(";")
    flat = [v.strip() for sublist in values for v in sublist if v.strip()]
    return pd.Series(Counter(flat)).sort_values(ascending=False)


def generate_report():
    """Generate the comprehensive analysis report."""
    print("=" * 60)
    print("  Phase 5: Analysis Report Generation")
    print("=" * 60)

    # Load data
    classified_path = DATA_DIR / "classified_papers.csv"
    accuracy_path = DATA_DIR / "accuracy_data.csv"

    if not classified_path.exists():
        print(f"  ❌ File not found: {classified_path}")
        print("  Run 02_classify_papers.py first.")
        return

    df = pd.read_csv(classified_path, encoding="utf-8-sig")
    print(f"  Loaded {len(df)} classified papers")

    # Load accuracy data if available
    has_accuracy = accuracy_path.exists()
    if has_accuracy:
        df_acc = pd.read_csv(accuracy_path, encoding="utf-8-sig")
        print(f"  Loaded {len(df_acc)} papers with accuracy data")
    else:
        df_acc = pd.DataFrame()
        print("  ⚠️  No accuracy data found. Skipping accuracy analysis.")

    # -----------------------------------------------------------------------
    # Compute statistics
    # -----------------------------------------------------------------------
    total_papers = len(df)
    year_min = int(df["year"].min()) if "year" in df.columns else "N/A"
    year_max = int(df["year"].max()) if "year" in df.columns else "N/A"

    # Year distribution
    year_counts = df["year"].value_counts().sort_index()

    # Sensor statistics
    sensor_counts = explode_column(df, "sensors")
    
    # Algorithm statistics
    algo_counts = explode_column(df, "algorithms")

    # Application statistics
    app_counts = explode_column(df, "applications")

    # Environment statistics
    env_counts = explode_column(df, "environments")

    # Dataset statistics
    ds_counts = explode_column(df, "datasets")

    # Top venues
    venue_counts = df["publication"].value_counts().head(15)

    # Papers with classification
    papers_with_sensor = df["sensors"].notna().sum()
    papers_with_algo = df["algorithms"].notna().sum()
    papers_with_app = df["applications"].notna().sum()
    papers_with_env = df["environments"].notna().sum()
    papers_with_ds = df["datasets"].notna().sum()

    # Co-occurrence analysis: top sensor-algorithm pairs
    cooccurrence = Counter()
    for _, row in df.iterrows():
        sensors = [s.strip() for s in str(row.get("sensors", "")).split(";") if s.strip()]
        algorithms = [a.strip() for a in str(row.get("algorithms", "")).split(";") if a.strip()]
        for s in sensors:
            for a in algorithms:
                cooccurrence[(s, a)] += 1
    top_pairs = cooccurrence.most_common(20)

    # Citation statistics
    if "citation_count" in df.columns:
        df["citation_count"] = pd.to_numeric(df["citation_count"], errors="coerce").fillna(0).astype(int)
        total_citations = df["citation_count"].sum()
        avg_citations = df["citation_count"].mean()
        max_citations = df["citation_count"].max()
        most_cited = df.nlargest(10, "citation_count")[["title", "year", "citation_count", "doi"]]
    else:
        total_citations = avg_citations = max_citations = 0
        most_cited = pd.DataFrame()

    # -----------------------------------------------------------------------
    # Build the report
    # -----------------------------------------------------------------------
    report_lines = []
    
    def add(line=""):
        report_lines.append(line)
    
    add("# 📊 Systematic Literature Review — Analysis Report")
    add(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    add(f"**Dataset:** {total_papers} papers ({year_min}–{year_max})")
    add(f"**Topic:** GNSS-Denied Localization for Autonomous Vehicles")
    add()
    add("---")
    add()

    # --- Section 1: Summary Statistics ---
    add("## 1. Summary Statistics")
    add()
    add("| Metric | Value |")
    add("|--------|-------|")
    add(f"| Total papers analysed | {total_papers} |")
    add(f"| Year range | {year_min}–{year_max} |")
    add(f"| Unique publication venues | {df['publication'].nunique()} |")
    add(f"| Papers with sensor classification | {papers_with_sensor} ({papers_with_sensor/total_papers*100:.1f}%) |")
    add(f"| Papers with algorithm classification | {papers_with_algo} ({papers_with_algo/total_papers*100:.1f}%) |")
    add(f"| Papers with application classification | {papers_with_app} ({papers_with_app/total_papers*100:.1f}%) |")
    add(f"| Papers with environment classification | {papers_with_env} ({papers_with_env/total_papers*100:.1f}%) |")
    add(f"| Papers referencing benchmark datasets | {papers_with_ds} ({papers_with_ds/total_papers*100:.1f}%) |")
    add(f"| Total citations | {total_citations:,} |")
    add(f"| Average citations per paper | {avg_citations:.1f} |")
    add(f"| Most cited paper | {max_citations} citations |")
    add()

    # --- Section 2: Publication Trends ---
    add("## 2. Publication Trends (RQ — Context)")
    add()
    add("### Papers per Year")
    add()
    add("| Year | Papers | Cumulative |")
    add("|------|--------|------------|")
    cumulative = 0
    for year in sorted(year_counts.index):
        count = year_counts[year]
        cumulative += count
        add(f"| {year} | {count} | {cumulative} |")
    add()
    add(f"![Papers per Year](figures/fig01_papers_per_year.png)")
    add()

    # --- Section 3: Sensor Analysis (RQ1) ---
    add("## 3. Sensor Modality Analysis (RQ1)")
    add()
    add("### Sensor Usage Frequency")
    add()
    add("| Sensor | Count | Percentage |")
    add("|--------|-------|------------|")
    for sensor, count in sensor_counts.items():
        pct = count / total_papers * 100
        add(f"| {sensor} | {count} | {pct:.1f}% |")
    add()
    add(f"![Sensor Usage](figures/fig02_sensor_usage.png)")
    add()
    if len(sensor_counts) > 0:
        top_sensor = sensor_counts.index[0]
        add(f"**Key Finding:** The most commonly used sensor modality is **{top_sensor}** "
            f"(appearing in {sensor_counts.iloc[0]} papers, {sensor_counts.iloc[0]/total_papers*100:.1f}% of the corpus). ")
        if len(sensor_counts) >= 3:
            add(f"The top three sensors are **{sensor_counts.index[0]}**, **{sensor_counts.index[1]}**, "
                f"and **{sensor_counts.index[2]}**.")
    add()

    # --- Section 4: Algorithm Analysis (RQ2) ---
    add("## 4. Algorithm & Framework Analysis (RQ2)")
    add()
    add("### Algorithm Usage Frequency")
    add()
    add("| Algorithm | Count | Percentage |")
    add("|-----------|-------|------------|")
    for algo, count in algo_counts.items():
        pct = count / total_papers * 100
        add(f"| {algo} | {count} | {pct:.1f}% |")
    add()
    add(f"![Algorithm Usage](figures/fig03_algorithm_usage.png)")
    add()
    add(f"![Algorithm Trends](figures/fig07_temporal_trends_algorithms.png)")
    add()
    if len(algo_counts) > 0:
        top_algo = algo_counts.index[0]
        add(f"**Key Finding:** The most widely adopted algorithm/framework is **{top_algo}** "
            f"({algo_counts.iloc[0]} papers). ")
    add()

    # --- Section 5: Sensor–Algorithm Co-occurrence (RQ1+RQ2) ---
    add("## 5. Sensor–Algorithm Co-occurrence Analysis (RQ1 + RQ2)")
    add()
    add("### Top 20 Sensor–Algorithm Combinations")
    add()
    add("| Rank | Sensor | Algorithm | Count |")
    add("|------|--------|-----------|-------|")
    for rank, ((sensor, algo), count) in enumerate(top_pairs, 1):
        add(f"| {rank} | {sensor} | {algo} | {count} |")
    add()
    add(f"![Co-occurrence Heatmap](figures/fig05_sensor_algorithm_heatmap.png)")
    add()
    if top_pairs:
        best_pair = top_pairs[0]
        add(f"**Key Finding:** The most common sensor–algorithm combination is "
            f"**{best_pair[0][0]} + {best_pair[0][1]}** ({best_pair[1]} papers).")
    add()
    add(f"![Temporal Trends](figures/fig06_temporal_trends_sensors.png)")
    add()

    # --- Section 6: Accuracy Analysis (RQ3) ---
    add("## 6. Localization Accuracy Analysis (RQ3)")
    add()
    if has_accuracy and len(df_acc) > 0:
        add(f"Accuracy values were extracted from {len(df_acc)} paper abstracts.")
        add()
        if "accuracy_m" in df_acc.columns:
            acc_values = pd.to_numeric(df_acc["accuracy_m"], errors="coerce").dropna()
            if len(acc_values) > 0:
                add("| Statistic | Value (m) |")
                add("|-----------|-----------|")
                add(f"| Papers with extractable accuracy | {len(acc_values)} |")
                add(f"| Mean accuracy | {acc_values.mean():.4f} |")
                add(f"| Median accuracy | {acc_values.median():.4f} |")
                add(f"| Min (best) accuracy | {acc_values.min():.4f} |")
                add(f"| Max (worst) accuracy | {acc_values.max():.4f} |")
                add(f"| Std deviation | {acc_values.std():.4f} |")
                add()
                
                # Accuracy by sensor
                if "sensors" in df_acc.columns:
                    add("### Accuracy by Sensor Type")
                    add()
                    add("| Sensor | Papers | Mean (m) | Median (m) | Best (m) |")
                    add("|--------|--------|----------|------------|----------|")
                    for _, row in df_acc.iterrows():
                        sensors_list = str(row.get("sensors", "")).split(";")
                    # Group by sensor
                    sensor_acc = {}
                    for _, row in df_acc.iterrows():
                        val = pd.to_numeric(row.get("accuracy_m"), errors="coerce")
                        if pd.isna(val):
                            continue
                        sensors_list = [s.strip() for s in str(row.get("sensors", "")).split(";") if s.strip()]
                        for s in sensors_list:
                            if s not in sensor_acc:
                                sensor_acc[s] = []
                            sensor_acc[s].append(val)
                    for s in sorted(sensor_acc, key=lambda x: np.mean(sensor_acc[x])):
                        vals = sensor_acc[s]
                        if len(vals) >= 2:
                            add(f"| {s} | {len(vals)} | {np.mean(vals):.4f} | {np.median(vals):.4f} | {np.min(vals):.4f} |")
                    add()
                
                if (FIGURES_DIR / "fig11_accuracy_by_sensor.png").exists():
                    add(f"![Accuracy by Sensor](figures/fig11_accuracy_by_sensor.png)")
                    add()
                if (FIGURES_DIR / "fig12_accuracy_by_algorithm.png").exists():
                    add(f"![Accuracy by Algorithm](figures/fig12_accuracy_by_algorithm.png)")
                    add()
    else:
        add("*Accuracy data was not available or could not be extracted from abstracts.*")
        add("*Note: Many papers report accuracy only in body text, not in abstracts.*")
    add()

    # --- Section 7: Application Domains (RQ4) ---
    add("## 7. Application Domain Analysis (RQ4)")
    add()
    add("| Application | Count | Percentage |")
    add("|-------------|-------|------------|")
    for app, count in app_counts.items():
        pct = count / total_papers * 100
        add(f"| {app} | {count} | {pct:.1f}% |")
    add()
    add(f"![Application Domains](figures/fig04_application_domains.png)")
    add()

    # --- Section 8: Environment Analysis (RQ4) ---
    add("## 8. Evaluation Environment Analysis (RQ4)")
    add()
    add("| Environment | Count | Percentage |")
    add("|-------------|-------|------------|")
    for env, count in env_counts.items():
        pct = count / total_papers * 100
        add(f"| {env} | {count} | {pct:.1f}% |")
    add()
    add(f"![Environment Distribution](figures/fig08_environment_distribution.png)")
    add()

    # --- Section 9: Datasets and Venues (RQ5) ---
    add("## 9. Benchmark Datasets & Publication Venues (RQ5)")
    add()
    add("### Benchmark Datasets")
    add()
    add("| Dataset | Count |")
    add("|---------|-------|")
    for ds, count in ds_counts.items():
        add(f"| {ds} | {count} |")
    add()
    add(f"![Top Datasets](figures/fig10_top_datasets.png)")
    add()
    add("### Top 15 Publication Venues")
    add()
    add("| Venue | Papers |")
    add("|-------|--------|")
    for venue, count in venue_counts.items():
        add(f"| {venue} | {count} |")
    add()
    add(f"![Top Venues](figures/fig09_top_venues.png)")
    add()

    # --- Section 10: Most Cited Papers ---
    add("## 10. Most Cited Papers")
    add()
    if len(most_cited) > 0:
        add("| Rank | Title | Year | Citations |")
        add("|------|-------|------|-----------|")
        for rank, (_, row) in enumerate(most_cited.iterrows(), 1):
            title_short = str(row["title"])[:80] + ("..." if len(str(row["title"])) > 80 else "")
            add(f"| {rank} | {title_short} | {row['year']} | {row['citation_count']} |")
    add()

    # --- Section 11: Key Findings Summary (RQ6) ---
    add("## 11. Key Findings & Answers to Research Questions")
    add()
    add("### RQ1: Sensor Modalities")
    if len(sensor_counts) >= 3:
        add(f"- The three most prevalent sensor modalities are **{sensor_counts.index[0]}** "
            f"({sensor_counts.iloc[0]}), **{sensor_counts.index[1]}** ({sensor_counts.iloc[1]}), "
            f"and **{sensor_counts.index[2]}** ({sensor_counts.iloc[2]}).")
        add(f"- {len(sensor_counts)} distinct sensor categories were identified across {papers_with_sensor} papers.")
    add()
    add("### RQ2: Algorithms & Frameworks")
    if len(algo_counts) >= 3:
        add(f"- The three most adopted algorithms are **{algo_counts.index[0]}** "
            f"({algo_counts.iloc[0]}), **{algo_counts.index[1]}** ({algo_counts.iloc[1]}), "
            f"and **{algo_counts.index[2]}** ({algo_counts.iloc[2]}).")
    add()
    add("### RQ3: Localization Accuracy")
    if has_accuracy and len(df_acc) > 0:
        acc_vals = pd.to_numeric(df_acc.get("accuracy_m", pd.Series()), errors="coerce").dropna()
        if len(acc_vals) > 0:
            add(f"- Accuracy values were extractable from {len(acc_vals)} papers.")
            add(f"- Median reported accuracy: **{acc_vals.median():.3f} m**.")
            add(f"- Best reported accuracy: **{acc_vals.min():.4f} m** ({acc_vals.min()*100:.2f} cm).")
    else:
        add("- Accuracy extraction from abstracts yielded limited results. Full-text analysis recommended.")
    add()
    add("### RQ4: Evaluation Environments")
    if len(env_counts) > 0:
        add(f"- Most papers evaluate in **{env_counts.index[0]}** environments ({env_counts.iloc[0]} papers).")
    add()
    add("### RQ5: Datasets & Venues")
    if len(ds_counts) > 0:
        add(f"- The most referenced benchmark dataset is **{ds_counts.index[0]}** ({ds_counts.iloc[0]} papers).")
    if len(venue_counts) > 0:
        add(f"- The top publication venue is **{venue_counts.index[0]}** ({venue_counts.iloc[0]} papers).")
    add()
    add("### RQ6: Best Sensor–Algorithm Combination")
    if top_pairs:
        add(f"- Based on frequency analysis, the most common combination is "
            f"**{top_pairs[0][0][0]} + {top_pairs[0][0][1]}** ({top_pairs[0][1]} papers).")
        if len(top_pairs) >= 3:
            add(f"- Top 3 combinations: "
                f"{top_pairs[0][0][0]}+{top_pairs[0][0][1]} ({top_pairs[0][1]}), "
                f"{top_pairs[1][0][0]}+{top_pairs[1][0][1]} ({top_pairs[1][1]}), "
                f"{top_pairs[2][0][0]}+{top_pairs[2][0][1]} ({top_pairs[2][1]}).")
    add()
    add("---")
    add()
    add("*This report was automatically generated by the GNSS-Denied Localization SLR Pipeline.*")
    add(f"*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')}*")

    # -----------------------------------------------------------------------
    # Save report
    # -----------------------------------------------------------------------
    report_path = OUTPUT_DIR / "report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\n  ✅ Report saved to: {report_path}")
    print(f"  📄 Report length: {len(report_lines)} lines")


if __name__ == "__main__":
    generate_report()
