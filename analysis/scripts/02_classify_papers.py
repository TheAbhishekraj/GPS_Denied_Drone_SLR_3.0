#!/usr/bin/env python3
"""
02_classify_papers.py — Keyword-Based Classification for GNSS-Denied Drone SLR
================================================================================

This script performs the second stage of the Systematic Literature Review pipeline:
  1. Loads the cleaned dataset from data/processed/database_final.csv
  2. Classifies each paper across five taxonomic dimensions using regex-based
     keyword dictionaries:
       - Sensors (18 categories)
       - Algorithms (20 categories)
       - Applications (12 categories)
       - Environments (8 categories)
       - Datasets (12 categories)
  3. Prints classification statistics and sample papers
  4. Saves classified data and summary report

All regex patterns use word boundaries (\\b) and case-insensitive matching
to minimize false positives from partial string matches.

Output:
  - data/processed/classified_papers.csv
  - analysis/output/checkpoint2_summary.txt

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
INPUT_CSV = BASE_DIR / "data" / "processed" / "database_final.csv"
OUTPUT_CSV = BASE_DIR / "data" / "processed" / "classified_papers.csv"
OUTPUT_DIR = BASE_DIR / "analysis" / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAXONOMY DICTIONARIES
# Each maps a category name → list of regex patterns (with word boundaries)
# ═══════════════════════════════════════════════════════════════════════════════

SENSOR_DICT = {
    "LiDAR": [
        r"\blidar\b", r"\blaser scanner\b", r"\bvelodyne\b",
        r"\bouster\b", r"\blivox\b", r"\blidar point cloud\b",
    ],
    "Camera": [
        r"\bcamera\b", r"\bvision\b", r"\bvisual\b",
        r"\bimage-based\b", r"\boptical flow\b",
    ],
    "Monocular": [
        r"\bmonocular\b", r"\bsingle camera\b", r"\bmonocular camera\b",
    ],
    "Stereo": [
        r"\bstereo camera\b", r"\bstereo vision\b",
        r"\bbinocular\b", r"\bstereoscopic\b",
    ],
    "RGB-D": [
        r"\brgb-d\b", r"\brgbd\b", r"\bdepth camera\b",
        r"\brealsense\b", r"\bkinect\b", r"\bstructured light\b",
    ],
    "Thermal": [
        r"\bthermal camera\b", r"\binfrared camera\b", r"\bflir\b",
        r"\bthermal imaging\b", r"\bthermal sensor\b",
    ],
    "Event Camera": [
        r"\bevent camera\b", r"\bdynamic vision sensor\b", r"\bdvs\b",
        r"\bevent-based camera\b", r"\bneuromorphic\b",
    ],
    "IMU": [
        r"\bimu\b", r"\binertial measurement unit\b", r"\binertial\b",
        r"\baccelerometer\b", r"\bgyroscope\b", r"\bmems imu\b",
        r"\binertial sensor\b", r"\binertial navigation\b",
    ],
    "UWB": [
        r"\buwb\b", r"\bultra-wideband\b", r"\bultra wideband\b",
        r"\bultra wide band\b",
    ],
    "Radar": [
        r"\bradar\b", r"\bmmwave\b", r"\bmillimeter wave\b",
        r"\bfmcw\b", r"\bsynthetic aperture radar\b", r"\bsar radar\b",
    ],
    "WiFi": [
        r"\bwifi\b", r"\bwi-fi\b", r"\brss\b", r"\brssi\b",
        r"\bfingerprint\b", r"\bwireless signal\b",
    ],
    "Barometer": [
        r"\bbarometer\b", r"\bbarometric\b", r"\bpressure sensor\b",
        r"\baltimeter\b",
    ],
    "Magnetometer": [
        r"\bmagnetometer\b", r"\bcompass\b", r"\bmagnetic field\b",
        r"\bmagnetic sensor\b",
    ],
    "Wheel Encoder": [
        r"\bwheel encoder\b", r"\bodometer\b", r"\bwheel speed\b",
        r"\bwheel odometry\b", r"\bencoder\b",
    ],
    "DVL": [
        r"\bdvl\b", r"\bdoppler velocity log\b", r"\bdoppler velocity\b",
    ],
    "Ultrasonic": [
        r"\bultrasonic\b", r"\bsonar\b", r"\bultrasound\b",
        r"\bacoustic sensor\b",
    ],
    "GNSS/GPS": [
        r"\bgnss\b", r"\bgps\b", r"\bsatellite navigation\b",
        r"\bglobal positioning\b", r"\bgnss receiver\b",
    ],
    "BLE/Bluetooth": [
        r"\bbluetooth\b", r"\bble\b", r"\bbeacon\b", r"\bibeacon\b",
    ],
}

ALGORITHM_DICT = {
    "EKF": [
        r"\bekf\b", r"\bextended kalman filter\b", r"\bextended kalman\b",
    ],
    "UKF": [
        r"\bukf\b", r"\bunscented kalman filter\b",
    ],
    "Particle Filter": [
        r"\bparticle filter\b", r"\bmonte carlo localization\b",
        r"\bsequential monte carlo\b", r"\bpf\b",
    ],
    "Factor Graph": [
        r"\bfactor graph\b", r"\bgraphical model\b",
        r"\bfactor graph optimization\b",
    ],
    "GTSAM": [
        r"\bgtsam\b",
    ],
    "ORB-SLAM": [
        r"\borb-slam\b", r"\borbslam\b", r"\borb slam\b",
    ],
    "VINS": [
        r"\bvins\b", r"\bvins-mono\b", r"\bvins-fusion\b",
        r"\bvins mono\b", r"\bvins fusion\b",
    ],
    "LIO-SAM": [
        r"\blio-sam\b", r"\bliosam\b", r"\blio sam\b",
    ],
    "LOAM": [
        r"\bloam\b", r"\blidar odometry and mapping\b",
        r"\ba-loam\b", r"\blego-loam\b", r"\bf-loam\b",
    ],
    "ICP": [
        r"\bicp\b", r"\biterative closest point\b",
    ],
    "NDT": [
        r"\bndt\b", r"\bnormal distribution transform\b",
        r"\bnormal distributions transform\b",
    ],
    "Bundle Adjustment": [
        r"\bbundle adjustment\b",
    ],
    "Visual Odometry": [
        r"\bvisual odometry\b",
    ],
    "Visual-Inertial Odometry": [
        r"\bvisual inertial odometry\b", r"\bvio\b", r"\bvisual-inertial\b",
    ],
    "Deep Learning": [
        r"\bdeep learning\b", r"\bcnn\b", r"\bconvolutional neural\b",
        r"\bneural network\b", r"\btransformer\b",
        r"\breinforcement learning\b", r"\blstm\b", r"\brnn\b",
        r"\bautoencoder\b", r"\bgan\b", r"\bself-supervised\b",
        r"\bend-to-end learning\b",
    ],
    "Optical Flow": [
        r"\boptical flow\b",
    ],
    "Complementary Filter": [
        r"\bcomplementary filter\b",
    ],
    "MSCKF": [
        r"\bmsckf\b", r"\bmulti-state constraint\b",
    ],
    "Pose Graph": [
        r"\bpose graph optimization\b", r"\bpose graph\b",
    ],
    "iSAM": [
        r"\bisam\b", r"\bisam2\b", r"\bincremental smoothing\b",
    ],
}

APPLICATION_DICT = {
    "UAV/Drone": [
        r"\buav\b", r"\bdrone\b", r"\bquadrotor\b", r"\bquadcopter\b",
        r"\bmav\b", r"\bunmanned aerial\b", r"\bmultirotor\b",
        r"\bhexarotor\b", r"\boctorotor\b", r"\bflying robot\b",
        r"\baerial vehicle\b", r"\baerial robot\b",
    ],
    "UGV": [
        r"\bugv\b", r"\bground vehicle\b", r"\bground robot\b",
        r"\bunmanned ground\b", r"\brover\b", r"\bmobile robot\b",
        r"\bwheeled robot\b",
    ],
    "AUV/Underwater": [
        r"\bauv\b", r"\bunderwater\b", r"\bsubmarine\b", r"\brov\b",
        r"\bmarine\b", r"\bsubsea\b", r"\bunderwater vehicle\b",
    ],
    "Pedestrian/PDR": [
        r"\bpedestrian\b", r"\bpdr\b", r"\bhuman\b", r"\bwearable\b",
        r"\bwalking\b", r"\bfoot-mounted\b", r"\bpedestrian dead reckoning\b",
    ],
    "Autonomous Car": [
        r"\bautonomous vehicle\b", r"\bself-driving\b", r"\bautonomous car\b",
        r"\bautomotive\b", r"\bconnected vehicle\b",
    ],
    "Multi-Robot/Swarm": [
        r"\bmulti-robot\b", r"\bswarm\b", r"\bcooperative\b",
        r"\bcollaborative\b", r"\bmulti-agent\b", r"\bformation\b",
        r"\bdistributed\b",
    ],
    "Agricultural": [
        r"\bagriculture\b", r"\bfarming\b", r"\bcrop\b",
        r"\bfield robot\b", r"\bprecision agriculture\b",
    ],
    "Inspection": [
        r"\binspection\b", r"\binfrastructure\b", r"\bbridge\b",
        r"\bpipeline\b", r"\bpower line\b", r"\bstructural health\b",
    ],
    "Indoor Robot": [
        r"\bindoor robot\b", r"\bservice robot\b", r"\bwarehouse\b",
        r"\blogistics\b", r"\bdelivery robot\b",
    ],
    "Search & Rescue": [
        r"\bsearch and rescue\b", r"\bsar\b", r"\bdisaster\b",
        r"\bemergency\b", r"\bfirst responder\b",
    ],
    "Spacecraft": [
        r"\bspacecraft\b", r"\bsatellite\b", r"\bspace\b",
        r"\borbital\b", r"\blunar\b",
    ],
    "Generic/Other": [],  # Fallback — assigned if no other category matches
}

ENVIRONMENT_DICT = {
    "Indoor": [
        r"\bindoor\b", r"\broom\b", r"\bbuilding\b", r"\bwarehouse\b",
        r"\bcorridor\b", r"\bhall\b", r"\blaboratory\b", r"\boffice\b",
    ],
    "Outdoor": [
        r"\boutdoor\b", r"\bfield\b", r"\bopen air\b",
        r"\bopen area\b", r"\bopen environment\b",
    ],
    "Urban": [
        r"\burban\b", r"\bcity\b", r"\bstreet\b", r"\broad\b",
        r"\bhighway\b", r"\bintersection\b",
    ],
    "Forest/Vegetation": [
        r"\bforest\b", r"\bvegetation\b", r"\bcanopy\b",
        r"\bwoodland\b", r"\btree\b", r"\bagricultural field\b",
    ],
    "Tunnel/Underground": [
        r"\btunnel\b", r"\bunderground\b", r"\bmine\b",
        r"\bcave\b", r"\bsubterranean\b", r"\bsubway\b",
    ],
    "Underwater": [
        r"\bunderwater\b", r"\bsubsea\b", r"\bmarine\b",
        r"\bocean\b", r"\blake\b", r"\briver\b",
    ],
    "Simulation": [
        r"\bsimulation\b", r"\bsimulated\b", r"\bgazebo\b",
        r"\bairsim\b", r"\bunreal\b", r"\bmatlab\b", r"\bcarla\b",
        r"\bflightmare\b", r"\brotors\b",
    ],
    "Real-World": [
        r"\breal-world\b", r"\breal world\b", r"\bexperiment\b",
        r"\bfield test\b", r"\bflight test\b", r"\breal environment\b",
        r"\bhardware experiment\b",
    ],
}

DATASET_DICT = {
    "KITTI": [r"\bkitti\b"],
    "EuRoC": [r"\beuroc\b", r"\beuroc mav\b"],
    "TUM": [r"\btum\b", r"\btum rgbd\b", r"\btum vi\b"],
    "Oxford RobotCar": [r"\boxford robotcar\b", r"\brobotcar\b"],
    "NCLT": [r"\bnclt\b"],
    "KAIST": [r"\bkaist\b"],
    "MulRan": [r"\bmulran\b"],
    "NTU VIRAL": [r"\bntu viral\b"],
    "Newer College": [r"\bnewer college\b"],
    "Custom/Own": [
        r"\bown dataset\b", r"\bcustom dataset\b", r"\bour dataset\b",
        r"\bcollected dataset\b", r"\bproprietary dataset\b",
        r"\bself-collected\b",
    ],
    "OpenLORIS": [r"\bopenloris\b"],
    "SubT": [r"\bsubt\b", r"\bsubterranean challenge\b", r"\bdarpa subterranean\b"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSIFICATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def precompile_dict(taxonomy: dict) -> dict:
    """Pre-compile regex patterns for performance."""
    compiled = {}
    for category, patterns in taxonomy.items():
        compiled[category] = [re.compile(p, re.IGNORECASE) for p in patterns]
    return compiled


def classify_text(text: str, compiled_dict: dict, fallback_category: str = None) -> str:
    """
    Match text against a compiled taxonomy dictionary.

    Returns semicolon-separated string of matched category names.
    If no match and fallback_category is provided, returns the fallback.
    """
    if not isinstance(text, str) or not text.strip():
        return fallback_category or ""

    matches = []
    for category, patterns in compiled_dict.items():
        if not patterns:  # Skip empty pattern lists (e.g., Generic/Other)
            continue
        for pat in patterns:
            if pat.search(text):
                matches.append(category)
                break  # One match per category is enough

    if not matches and fallback_category:
        return fallback_category

    return "; ".join(matches)


def main():
    """Run the keyword-based classification pipeline."""
    print("=" * 72)
    print("  02_classify_papers.py — GNSS-Denied Drone SLR Classification")
    print("=" * 72)

    # ── 1. Load cleaned data ──────────────────────────────────────────────
    print(f"\n[1/5] Loading cleaned data: {INPUT_CSV}")
    if not INPUT_CSV.exists():
        print(f"  ERROR: File not found → {INPUT_CSV}")
        print("  Run 01_clean_data.py first.")
        sys.exit(1)

    df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
    print(f"  Loaded {len(df)} papers")

    # Ensure text_corpus exists
    if "text_corpus" not in df.columns:
        print("  WARNING: text_corpus column not found, rebuilding...")
        for col in ("title", "abstract", "author_keywords", "ieee_terms"):
            if col in df.columns:
                df[col] = df[col].fillna("")
        df["text_corpus"] = (
            df["title"].astype(str) + " " +
            df["abstract"].astype(str) + " " +
            df["author_keywords"].astype(str) + " " +
            df["ieee_terms"].astype(str)
        ).str.lower()

    # ── 2. Pre-compile all dictionaries ───────────────────────────────────
    print("\n[2/5] Pre-compiling taxonomy dictionaries...")
    sensor_compiled = precompile_dict(SENSOR_DICT)
    algo_compiled = precompile_dict(ALGORITHM_DICT)
    app_compiled = precompile_dict(APPLICATION_DICT)
    env_compiled = precompile_dict(ENVIRONMENT_DICT)
    dataset_compiled = precompile_dict(DATASET_DICT)
    print(f"  Sensors:      {len(SENSOR_DICT)} categories, "
          f"{sum(len(v) for v in SENSOR_DICT.values())} patterns")
    print(f"  Algorithms:   {len(ALGORITHM_DICT)} categories, "
          f"{sum(len(v) for v in ALGORITHM_DICT.values())} patterns")
    print(f"  Applications: {len(APPLICATION_DICT)} categories, "
          f"{sum(len(v) for v in APPLICATION_DICT.values())} patterns")
    print(f"  Environments: {len(ENVIRONMENT_DICT)} categories, "
          f"{sum(len(v) for v in ENVIRONMENT_DICT.values())} patterns")
    print(f"  Datasets:     {len(DATASET_DICT)} categories, "
          f"{sum(len(v) for v in DATASET_DICT.values())} patterns")

    # ── 3. Classify each paper ────────────────────────────────────────────
    print("\n[3/5] Classifying papers...")

    df["sensors"] = df["text_corpus"].apply(
        lambda t: classify_text(t, sensor_compiled)
    )
    print("  ✓ Sensors classified")

    df["algorithms"] = df["text_corpus"].apply(
        lambda t: classify_text(t, algo_compiled)
    )
    print("  ✓ Algorithms classified")

    df["applications"] = df["text_corpus"].apply(
        lambda t: classify_text(t, app_compiled, fallback_category="Generic/Other")
    )
    print("  ✓ Applications classified")

    df["environments"] = df["text_corpus"].apply(
        lambda t: classify_text(t, env_compiled)
    )
    print("  ✓ Environments classified")

    df["datasets"] = df["text_corpus"].apply(
        lambda t: classify_text(t, dataset_compiled)
    )
    print("  ✓ Datasets classified")

    # ── 4. Compute and print statistics ───────────────────────────────────
    print("\n" + "=" * 72)
    print("  CLASSIFICATION STATISTICS")
    print("=" * 72)

    stats_lines = []

    def log(msg):
        print(msg)
        stats_lines.append(msg)

    total = len(df)
    has_sensor = (df["sensors"].str.strip() != "").sum()
    has_algo = (df["algorithms"].str.strip() != "").sum()
    has_app = (df["applications"].str.strip() != "").sum()
    has_env = (df["environments"].str.strip() != "").sum()
    has_dataset = (df["datasets"].str.strip() != "").sum()

    log(f"\n  Total papers: {total}")
    log(f"  Papers with ≥1 sensor:      {has_sensor}  ({100*has_sensor/total:.1f}%)")
    log(f"  Papers with ≥1 algorithm:   {has_algo}  ({100*has_algo/total:.1f}%)")
    log(f"  Papers with ≥1 application: {has_app}  ({100*has_app/total:.1f}%)")
    log(f"  Papers with ≥1 environment: {has_env}  ({100*has_env/total:.1f}%)")
    log(f"  Papers with ≥1 dataset:     {has_dataset}  ({100*has_dataset/total:.1f}%)")

    def distribution(col_name: str, label: str):
        """Compute and print category distribution for a semicolon-separated column."""
        log(f"\n  {label} Distribution (sorted by frequency):")
        log(f"  {'Category':<30s}  {'Count':>5s}  {'%':>6s}")
        log(f"  {'-'*30}  {'-'*5}  {'-'*6}")

        # Explode semicolon-separated values
        all_cats = (
            df[col_name]
            .dropna()
            .loc[lambda s: s.str.strip() != ""]
            .str.split(r";\s*")
            .explode()
            .str.strip()
            .loc[lambda s: s != ""]
        )
        cat_counts = all_cats.value_counts()

        for cat, cnt in cat_counts.items():
            pct = 100 * cnt / total
            log(f"  {cat:<30s}  {cnt:>5d}  {pct:>5.1f}%")

        return cat_counts

    sensor_dist = distribution("sensors", "SENSOR")
    algo_dist = distribution("algorithms", "ALGORITHM")
    app_dist = distribution("applications", "APPLICATION")
    env_dist = distribution("environments", "ENVIRONMENT")
    dataset_dist = distribution("datasets", "DATASET")

    # ── 5. Print sample papers ────────────────────────────────────────────
    print(f"\n\n  20 Random Classified Papers:")
    print("  " + "-" * 110)
    sample = df.sample(n=min(20, len(df)), random_state=42)
    for _, row in sample.iterrows():
        title_short = str(row["title"])[:80]
        if len(str(row["title"])) > 80:
            title_short += "..."
        print(f"  Title:   {title_short}")
        print(f"  Sensors: {row['sensors']}")
        print(f"  Algos:   {row['algorithms']}")
        print(f"  App:     {row['applications']}")
        print(f"  Env:     {row['environments']}")
        print(f"  Dataset: {row['datasets']}")
        print("  " + "-" * 110)

    # ── 6. Save classified data ───────────────────────────────────────────
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\n  ✓ Saved classified data → {OUTPUT_CSV}")
    print(f"    Rows: {len(df)}, Columns: {len(df.columns)}")

    # ── 7. Save summary report ────────────────────────────────────────────
    report_path = OUTPUT_DIR / "checkpoint2_summary.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("CHECKPOINT 2 — Classification Summary\n")
        f.write("=" * 60 + "\n")
        f.write(f"Date: 2026-07-12\n")
        f.write(f"Input: {INPUT_CSV.name}\n")
        f.write(f"Output: {OUTPUT_CSV.name}\n\n")
        for line in stats_lines:
            f.write(line.strip() + "\n")

        # Write co-occurrence summary
        f.write("\n\nSENSOR CO-OCCURRENCE (top pairs):\n")
        sensor_pairs = {}
        for _, row in df.iterrows():
            cats = [c.strip() for c in str(row["sensors"]).split(";") if c.strip()]
            for i in range(len(cats)):
                for j in range(i + 1, len(cats)):
                    pair = tuple(sorted([cats[i], cats[j]]))
                    sensor_pairs[pair] = sensor_pairs.get(pair, 0) + 1
        top_pairs = sorted(sensor_pairs.items(), key=lambda x: x[1], reverse=True)[:15]
        for (a, b), cnt in top_pairs:
            f.write(f"  {a} + {b}: {cnt}\n")

    print(f"  ✓ Saved summary report → {report_path}")

    print("\n" + "=" * 72)
    print("  Pipeline Stage 2 COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
