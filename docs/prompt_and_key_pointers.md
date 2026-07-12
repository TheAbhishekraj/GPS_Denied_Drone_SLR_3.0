# Master Prompt & Key Pointers Reference Guide

This document archives the core goals, objectives, and checkpoints of the Systematic Literature Review on GNSS-Denied Localization (Version 2.0).

---

## 1. Core Objectives
The objective of this Systematic Literature Review (SLR) is to process a database export of publications to answer:
- **What sensor–algorithm combinations are most commonly used for localization in GNSS-denied environments?**
- **Which combinations achieve the highest accuracy, for which applications (UAV, UGV, indoor, underwater, etc.)?**
- **What are the current trends, open challenges, and future research directions?**

---

## 2. Six Checkpoints (PDCA Cycle)

- **Checkpoint 1 (Data Cleaning):** Programmatic clean-up, year range filtering, duplicate checks, and inclusion screening. Present data table and 10 random sample rows.
- **Checkpoint 2 (Classification):** Pre-compiled keyword regex taxonomies for sensors, algorithms, application domains, environments, and benchmark datasets. Present 20 random classifications.
- **Checkpoint 3 (Statistical Analysis & Figures):** Production of 10 IEEE-standard high-resolution figures and 5 markdown tables detailing co-occurrence, temporal trends, and venue/dataset breakdowns.
- **Checkpoint 4 (Reference Extraction):** Building IEEE numbered bibliography, BibTeX citation library, and identifying high-impact papers.
- **Checkpoint 5 (Manuscript Writing):** Compiling a journal-ready publication manuscript (`paper_final.md`) with abstract, intro, methodology, results, discussion, and challenges, along with supplementary letters.
- **Final Checkpoint (Repository Packaging):** Generating `README.md`, orchestrators, dependency files, and documenting the entire process in a parallel learning logbook.

---

## 3. Key Pointers for SLR Replication

1.  **Platform Compatibility:** Reconfiguring standard Python terminals to UTF-8 using `sys.stdout.reconfigure(encoding='utf-8')` is vital on Windows machines to prevent character map encoding crashes when outputting Unicode characters (`✓`, `✗`, heatmaps, heat boxes).
2.  **Taxonomy Boundaries:** Using regex word boundaries (`\b`) is non-negotiable to prevent substring match corruption (e.g., matching "imu" inside "simulation" or "slam" inside "slamming").
3.  **Unified Text Corpus:** For keyword tagging, searching against a concatenated lower-case string of `title + abstract + author_keywords + ieee_terms` ensures that papers are correctly classified even if the abstract is brief.
4.  **Quantitative Unit Conversions:** Always normalize reported error values to a single unit (metres) before compiling statistical averages or boxplots. Keep distance-based errors separate from drift percentages.
5.  **BibTeX Key Uniqueness:** Track key counts chronologically to prevent compile collisions by appending suffixes (`a`, `b`, `c`) for duplicate author-year keys.
