# Reproducibility Protocol: GNSS-Denied Drone SLR 3.0

This guide provides a step-by-step protocol to replicate all data processing, classifications, figures, tables, and manuscript assets generated in this Systematic Literature Review.

---

## 💻 System Requirements

*   **Operating System:** Platform-agnostic (Windows, macOS, Linux).
*   **Language Environment:** Python 3.8 to Python 3.14.
*   **Hardware Profile:** Standard consumer laptop (Run time is extremely light, < 15 seconds).

---

## 🚀 Step-by-Step Replication

### 1. Environment Setup
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/TheAbhishekraj/GPS_Denied_Drone_SLR_3.0.git
cd GPS_Denied_Drone_SLR_3.0
```

It is recommended to use a virtual environment to isolate dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Install the exact pinned dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Processing Pipeline
Run the master orchestrator script to execute all 6 phases:
```bash
python analysis/scripts/run_all.py
```

### 3. Containerized Replication (Docker)
Alternatively, you can replicate the entire pipeline inside an isolated Docker container:
```bash
# Build the Docker image
docker build -t slr-pipeline .

# Run the pipeline container
docker run --name slr-container slr-pipeline
```

---

## 📊 Expected Outputs Validation

Upon successful execution, the following artifacts will be written or updated:

1.  **Datasets (`data/processed/`):**
    *   `database_final.csv`: 995 cleaned and screened publications.
    *   `classified_papers.csv`: 995 publications mapped to taxonomic tags.
    *   `accuracy_data.csv`: 44 publications with parsed quantitative translation errors.
2.  **Figures (`analysis/output/figures/`):**
    *   `fig01_papers_per_year.png` to `fig10_top_datasets.png`: Primary descriptive statistics.
    *   `fig11_accuracy_by_sensor.png` & `fig12_accuracy_by_algorithm.png`: Boxplots of localization errors.
3.  **Literature Statistics & Reports:**
    *   `analysis/output/tables.md`: 5 formatted markdown tables.
    *   `analysis/output/report.md`: Detailed SLR metrics.
    *   `references/bibliography.txt`: Standard IEEE bibliography.
    *   `references/references.bib`: Standard BibTeX references.
    *   `references/key_papers.md`: Registry of 463 high-impact papers.

*Expected Terminal Log Output:*
```text
======================================================================
  🎯 GNSS-Denied Localization — Systematic Literature Review Pipeline
======================================================================

======================================================================
  Step 1/6: Phase 1: Data Cleaning & Preparation
  Script: 01_clean_data.py
======================================================================
...
  ✅ Step 1 completed successfully in 0.5s

======================================================================
  Step 2/6: Phase 2: Paper Classification
  Script: 02_classify_papers.py
======================================================================
...
  ✅ Step 2 completed successfully in 1.2s

...
  ✅ Pipeline Summary
======================================================================
  ✅ Step 1: Phase 1: Data Cleaning & Preparation
  ✅ Step 2: Phase 2: Paper Classification
  ✅ Step 3: Phase 3: Figure Generation & Statistical Analysis
  ✅ Step 4: Phase 3b: Accuracy Extraction
  ✅ Step 5: Phase 4: Bibliography & Reference Building
  ✅ Step 6: Phase 5: Analysis Report Generation

  Total time: 8.5s
======================================================================
```
---

## 🔧 Troubleshooting & Platform Notes

### Windows Terminal Encoding Issue
If running on Windows PowerShell/CMD, python script print commands containing Unicode characters (like `✓` or `✗`) may raise `UnicodeEncodeError`. 
*   *Resolution:* All pipeline scripts are preconfigured to override default terminal mapping by forcing UTF-8:
    ```python
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ```

### Missing Raw Data
If `01_clean_data.py` complains about missing input files, verify that `data/raw/export2026.07.12-04.50.12.csv` exists and is untarred.
