# GNSS-Denied Localization Systematic Literature Review Pipeline

This repository contains the complete, reproducible pipeline for the Systematic Literature Review (SLR) on **GNSS-Denied Localization for Autonomous Vehicles (2015–2026)**.

The pipeline processes **995 peer-reviewed publications** from IEEE Xplore, performs taxonomic classification, generates publication-ready figures/tables, extracts localization accuracy metrics, builds bibliographies, and compiles a complete manuscript draft.

---

## 📂 Repository Structure

```
📁GPS_Denied_Drone_SLR 3.0/
├── README.md                               # Project overview, how to reproduce (this file)
├── requirements.txt                        # Python dependencies
├── data/
│   ├── raw/                                 # Original user files (CSV/Excel)
│   │   └── export2026.07.12-04.50.12.csv    # Raw IEEE Xplore export (1,000 papers)
│   └── processed/
│       ├── database_final.csv               # Cleaned dataset (995 papers)
│       ├── classified_papers.csv            # Papers with sensor/algorithm labels
│       └── accuracy_data.csv                # Extracted accuracy values (44 papers)
├── analysis/
│   ├── scripts/
│   │   ├── 01_clean_data.py                 # Phase 1: Data Cleaning & Screening
│   │   ├── 02_classify_papers.py            # Phase 2: Taxonomic Classification
│   │   ├── 03_generate_figures.py           # Phase 3: Figure & Table Generation
│   │   ├── 04_extract_accuracy.py           # Phase 3b: Accuracy Extraction
│   │   ├── 05_build_references.py           # Phase 4: Reference & Bibliography Builder
│   │   ├── 06_write_report.py               # Phase 5: Detailed Report Compiler
│   │   └── run_all.py                       # Master orchestrator script
│   └── output/
│       ├── figures/                         # 12 high-resolution PNG figures (300 DPI)
│       ├── report.md                        # Detailed analysis report
│       └── tables.md                        # Clean tables for manuscript
├── references/
│   ├── bibliography.txt                     # Numbered references (IEEE format)
│   ├── references.bib                       # Standard BibTeX file
│   └── key_papers.md                        # High-impact paper registry (463 papers)
├── manuscript/
│   ├── paper_final.md                       # Full review manuscript draft
│   ├── cover_letter.md                      # Journal cover letter template
│   ├── author_contributions.md              # Author roles (CRediT taxonomy)
│   ├── conflict_of_interest.md              # Declared interests statement
│   └── data_availability.md                 # Open-science data availability statement
├── docs/
│   ├── do_and_dont.md                       # SLR Do's and Don'ts best practices
│   ├── manual_current_literature.md         # Guide to high-impact papers
│   ├── review_methodology_phase_by_phase.md # Detailed methodology guide
│   ├── prompt_and_key_pointers.md           # Master prompt reference
│   └── learning_log.md                      # Parallel logbook (decisions & adjustments)
└── prisma/
    └── prisma_flow_diagram.md               # PRISMA flow diagram (Mermaid)
```

---

## 🚀 Quick Start & Replication

### Prerequisites
Make sure Python 3.8+ is installed on your system. Install the required libraries:
```bash
pip install -r requirements.txt
```

### Running the Complete Pipeline
You can re-run the entire pipeline from scratch with a single command:
```bash
python analysis/scripts/run_all.py
```

### Resuming or Running Specific Steps
If you make changes to a specific script, you can run only that script, or resume the pipeline from a specific step:
```bash
# Run only Step 2 (Classification)
python analysis/scripts/run_all.py --only 2

# Resume from Step 3 (Figure Generation)
python analysis/scripts/run_all.py --from 3
```

---

## 📊 Summary of Statistical Findings (995 Papers)

- **Publication Venues:** High-impact venues dominate, led by *IEEE Transactions on Instrumentation and Measurement* (56 papers), *IEEE Robotics and Automation Letters* (43 papers), and *IEEE Sensors Journal* (41 papers).
- **Core Sensors (RQ1):** Camera (40.4%, 402 papers), IMU (33.5%, 333 papers), and GNSS/GPS (32.3%, 321 papers) represent the primary sensing modalities.
- **Core Algorithms (RQ2):** Visual-Inertial Odometry (VIO) is the most popular estimation framework (14.0%, 139 papers), followed by Visual Odometry (VO) (12.9%, 128 papers) and Extended Kalman Filters (EKF) (12.0%, 119 papers). Deep Learning (12.0%, 119 papers) shows a massive upward trend.
- **Top Sensor-Algorithm Pair (RQ1 + RQ2):** Camera + VIO (138 papers) and IMU + VIO (137 papers) represent the most frequent sensor-fusion setups.
- **Reported Accuracy (RQ3):** synthesized from 41 papers with extractable metric errors:
  - Median error: **0.360 m**
  - Minimum error: **0.0050 m** (0.50 cm)
  - Top sensors by median accuracy: LiDAR (0.127 m), Radar (0.171 m), Camera (0.315 m), UWB (0.320 m).
- **Evaluation Environments (RQ4):** Indoor (28.2%, 281 papers) is the most common testing ground. A significant evaluation gap exists: while simulation is used in 19.8% of papers, only 18.5% verify their systems in real-world environments.
- **Benchmark Datasets (RQ5):** KITTI (44 papers) is the dominant benchmark dataset, followed by Custom/Own datasets (23 papers) and EuRoC (17 papers).
