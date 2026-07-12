# Review Methodology: Phase-by-Phase Execution Guide

This document outlines the systematic methodology implemented in the GNSS-Denied Localization Systematic Literature Review (SLR) pipeline to ensure transparency, rigour, and repeatability.

---

## Phase 1: Database Search and Data Preparation

### 1. Database Search
The literature search was executed on the **IEEE Xplore** digital library using the query:
```
("GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied")
AND ("UAV" OR "drone" OR "quadrotor" OR "MAV" OR "unmanned aerial")
AND ("navigation" OR "localization" OR "SLAM" OR "odometry" OR "state estimation")
```
This query returned **1,000 papers** (journal articles and conference proceedings) from 2015 to 2026.

### 2. Standardization & Metadata Clean-up
The raw export was loaded programmatically via `01_clean_data.py`:
- Column headers were standardized to clean names (e.g. `Document Title` to `title`, `Article Citation Count` to `citation_count`).
- Whitespace was normalized, HTML markup tags in abstracts were removed, and string fields were trimmed.
- The `year` column was parsed as integers. No records were found outside the target range of 2015–2026.
- The `citation_count` column was filled with 0 where NaN.

### 3. Inclusion and Exclusion Filtering
A unified lowercase `text_corpus` column was built by concatenating the title, abstract, and keyword fields.
- **Inclusion Screening:** A regex search checked for at least one of 22 key localization/navigation terms (e.g., `odometry`, `state estimation`, `SLAM`, `path planning`, `visual inertial`).
- **Exclusion Filtering:** 5 papers were excluded because they did not pass the inclusion screening (e.g., papers discussing power grid state estimation or cellular signal routing with no drone navigation context).
- **Final corpus size:** **995 papers**.

---

## Phase 2: Taxonomic Classification

The classification pipeline (`02_classify_papers.py`) applied pre-compiled regex dictionaries with word boundaries (`\b`) and case-insensitive matching across five taxonomic dimensions:

1.  **Sensor Modalities:** Classifies papers based on sensor hardware (e.g., LiDAR, Camera, IMU, UWB, Radar, WiFi, Barometer, Magnetometer, Wheel Encoder, DVL, Ultrasonic, GNSS/GPS, BLE/Bluetooth).
2.  **Estimation Algorithms:** Identifies algorithms used (e.g., EKF, UKF, Particle Filter, Factor Graph, GTSAM, ORB-SLAM, VINS, LIO-SAM, LOAM, ICP, NDT, Bundle Adjustment, VO, VIO, Deep Learning, MSCKF, Pose Graph, iSAM).
3.  **Application Domains:** Determines platform target (e.g., UAV/Drone, UGV, AUV/Underwater, Pedestrian/PDR, Autonomous Car, Multi-Robot/Swarm, Agricultural, Inspection, Indoor Robot, Search & Rescue, Spacecraft).
4.  **Evaluation Environments:** Classifies target testing grounds (e.g., Indoor, Outdoor, Urban, Forest/Vegetation, Tunnel/Underground, Underwater, Simulation, Real-World).
5.  **Benchmark Datasets:** Logs standardized datasets (e.g., KITTI, EuRoC, TUM, Oxford RobotCar, NCLT, KAIST, MulRan, NTU VIRAL, Newer College, Custom/Own, OpenLORIS, SubT).

Matches were saved as semicolon-separated strings in `classified_papers.csv` for multi-label analysis.

---

## Phase 3: Statistical Analysis & Visualization

### 1. Frequency Analysis
We calculated frequency counts for all taxonomies by exploding semicolon-separated fields.
- Over time trends were plotted to show temporal changes (e.g. comparing the growth of Deep Learning vs filtering-based EKF algorithms).
- Publication venues were ranked to identify the most active journals/conferences.

### 2. Sensor–Algorithm Co-occurrence Heatmap
Co-occurrence pairs (sensor × algorithm) were compiled for each paper. Heatmaps were plotted to show the most active research pairings (such as `Camera + VIO` or `IMU + EKF`).

### 3. Quantitative Accuracy Extraction (Meta-Analysis)
We searched abstracts using four regex patterns to isolate quantitative localization errors:
- Metric unit normalization: values in `cm` and `mm` were converted to `metres`.
- Separate tracking: distance-based absolute errors (`accuracy_m`) were tracked separately from percentage-based drift (`accuracy_pct`).
- Out of 995 papers, 41 distance-based values and 3 percentage-based values were extracted.
- Boxplots were generated to show the distribution of accuracy across different sensor types and algorithm classes (only including categories with $n \ge 3$ for statistical validity).

---

## Phase 4: Reference Building

Standardized references were compiled by `05_build_references.py`:
- **IEEE Format:** Generated `references/bibliography.txt`, sorting references chronologically and alphabetically, formatting author names to `F. Last` and truncating to `et al.` if there are more than 3 authors.
- **BibTeX Format:** Generated `references/references.bib` with auto-detected entry types (`@article` for journals, `@inproceedings` for conferences). Collision detection appended suffixes to duplicate keys.
- **High-Impact Identification:** Flagged papers with $\ge 10$ citations or published in top-tier venues (such as *IEEE Transactions*, *Robotics and Automation Letters*, *ICRA*, *IROS*, or *Sensors*) and logged them to `references/key_papers.md`.
