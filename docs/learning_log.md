# Learning Log: Decision and Technical Adjustments Logbook

This logbook documents the key technical decisions, classification dictionary updates, issues encountered, and resolutions implemented during the Systematic Literature Review (SLR) on GNSS-Denied Localization (2015–2026).

---

## 1. Cleaned Data & Inclusion/Exclusion Decisions (Phase 1)
- **Initial Dataset:** 1,000 papers exported from IEEE Xplore.
- **Deduplication:** We ran deduplication check using DOI and exact Title matching (case-insensitive). Interestingly, the export was clean with **0 duplicate DOIs** and **0 duplicate titles** because the IEEE search query was highly selective.
- **Year Check:** The papers span naturally between 2015 and 2026. All 1,000 papers fell within the target range (2015–2026), so no papers were dropped due to year constraints.
- **Inclusion/Exclusion Filtering:** 
  - *Decision:* We implemented a screening filter that checked the concatenated text corpus of `title + abstract + author_keywords + ieee_terms` against 22 localization-related keywords.
  - *Result:* **5 papers** were excluded during this step. These papers focused purely on power system state estimation or wireless communications routing protocols (e.g., using terms like "dynamic state estimation" in the context of power grids, or "signal routing" without any actual robot localization or odometry context).
  - *Final Cleaned Dataset:* **995 papers**.

---

## 2. Classification Taxonomy and Dictionary Refinements (Phase 2)
- **Sensor Dictionary Tuning:**
  - *Challenge:* Initial regex for "Camera" matching was capturing generic terms like "visual inspection" or "image transmission" which did not represent the camera as a positioning sensor.
  - *Adjustment:* Pre-compiled regex patterns were refined with strict word boundaries `\b` (e.g., `\bcamera\b`, `\bvision\b`, `\bvisual\b`). If a paper matched `monocular`, `stereo`, or `rgb-d`, it was also linked to the Camera category.
- **Algorithm Dictionary Tuning:**
  - *Challenge:* Semicolon separation of multi-valued classification results could create trailing spaces or duplicate terms.
  - *Adjustment:* Implemented a clean string join with `"; "` and stripped individual tokens before storing them.
  - *Result:* A clean cross-tabulation matrix where we can analyze top sensor-algorithm pairings (e.g., `Camera + VIO`, `IMU + EKF`).

---

## 3. Accuracy Extraction Performance & Challenges (Phase 3)
- **Abstract Metric Extraction:**
  - *Challenge:* Extracting quantitative errors from abstracts using regular expressions is notoriously difficult because authors report metrics in varied formats (e.g., "0.5m", "under 10 cm", "RMSE of 2%").
  - *Adjustment:* We designed 4 distinct regex patterns to capture different grammatical structures (e.g., `Metric -> Value -> Unit` vs `Value -> Unit -> Metric`).
  - *Result:* Out of 995 papers, **44 papers** had extractable quantitative accuracy metrics in their abstracts (4.4% extraction rate). This is a known limitation of SLR text mining, as many papers reserve raw numerical results for tables and plots in the main body.
  - *Action:* The extraction pipeline successfully handled units, converting `cm` and `mm` to `metres`. It successfully distinguished distance-based error (41 papers) from percentage-based drift (3 papers).
  - *Visualization:* With 41 data points, we successfully generated both `fig11_accuracy_by_sensor.png` and `fig12_accuracy_by_algorithm.png` using a minimum threshold of 3 papers per category to ensure statistical relevance.

---

## 4. Bibliography and BibTeX Generation (Phase 4)
- **Author List Formatting:**
  - *Challenge:* Raw IEEE author fields contain semicolon-separated names in different formats (e.g., "M. Wang; C. Zhai" vs "Barzegar, A.").
  - *Adjustment:* We wrote a robust author parser in `05_build_references.py` that split, standardized, and formatted authors as `F. M. Last` for IEEE bibliography, and kept first/middle initials.
  - *Duplicate Key Handling:*
    - *Decision:* For papers published by the same first author in the same year, we appended a suffix (e.g., `wang2019a`, `wang2019b`) to prevent BibTeX compilation collisions.

---

## 5. Lessons Learned for Future Systematic Reviews
1. **Consolidated Text Corpus:** Concatenating titles, abstracts, and keywords into a single lowercase `text_corpus` column is the most efficient way to run clean regex matching without losing context.
2. **Terminal Encoding Constraints:** On Windows, python print statements containing Unicode symbols (e.g. `✓`, `✗`) will crash with `UnicodeEncodeError` if the standard console is set to `cp1252`. Proactively reconfiguring stdout and stderr using `sys.stdout.reconfigure(encoding='utf-8')` is essential for platform-independent research scripts.
3. **Regex Word Boundaries:** Always use `\b` when matching sensor/algorithm names to prevent partial substring matches (e.g. preventing "slam" from matching "slamming" or "vins" from matching "provinces").
