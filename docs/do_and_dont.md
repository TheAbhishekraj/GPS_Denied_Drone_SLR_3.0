# Do's and Don'ts for Systematic Literature Reviews (SLRs) in Robotics

To maintain high data integrity and ensure journal publication quality, follow these guidelines when updating or expanding this systematic review.

## Do's

### 1. Data Cleaning & Preparation
- **DO** verify raw CSV column headers. Academic databases (IEEE Xplore, Scopus, Web of Science) change their export column names occasionally. Update the mapping dictionary in `01_clean_data.py` if headers mismatch.
- **DO** keep original casing and special characters in raw data, but convert to lowercase *only* when building the search corpus for regex matching.
- **DO** use `sys.stdout.reconfigure(encoding='utf-8')` in all scripts to avoid terminal crashes on Windows systems when printing unicode symbols.

### 2. Taxonomic Classification
- **DO** use word boundaries (`\b`) for all regex keyword patterns. This prevents false positive matches (e.g., matching "vins" against "provinces" or "slam" against "slamming").
- **DO** update keyword dictionaries as new sensors (e.g., solid-state LiDAR, neuromorphic event sensors) or algorithms (e.g., Neural Radiance Fields, 3D Gaussian Splatting for SLAM) gain traction in the literature.
- **DO** keep a fallback category (like `Generic/Other`) for application classification to avoid dropping papers that do not specify their robotic platform.

### 3. Quantitative Analysis
- **DO** convert all extracted numerical error values into a unified metric (metres for translation error). Double-check the scale conversion (e.g., dividing cm by 100, mm by 1000).
- **DO** restrict boxplots and statistical visualizations to categories that have at least 3 data points. Creating boxplots from 1 or 2 data points leads to poor statistical significance.

### 4. Bibliography and Code Representation
- **DO** ensure that every BibTeX entry has a unique key. Append letters (a, b, c) to first-author-lastname + year combinations to handle duplicates.
- **DO** write reproducible modular scripts (01 to 06) and provide a master orchestrator (`run_all.py`) to run them sequentially.

---

## Don'ts

### 1. Data Cleaning & Screening
- **DON'T** delete papers manually from the raw CSV. Always use programmatic filters (like year ranges or text boundaries) to keep the pipeline 100% reproducible.
- **DON'T** perform fuzzy title matching on very short titles (e.g., "UAV Navigation"), as it can cause false duplicate detection.

### 2. Taxonomy Matching
- **DON'T** use general keywords that are not specific enough. For example, using the keyword "filter" alone will match Kalman filters, particle filters, high-pass filters, and signal filters, leading to corrupt algorithm taxonomy.
- **DON'T** assume a paper uses only one sensor or algorithm. Always concatenate matches with a semicolon to represent multi-sensor fusion.

### 3. Accuracy Extraction
- **DON'T** mix distance-based translation error (in metres) with percentage-based drift (e.g., "% of trajectory") in the same column. Keep them in separate columns (`accuracy_m` and `accuracy_pct`).
- **DON'T** assume that a number in the abstract always represents localization error. The regex must verify that keywords like `RMSE`, `error`, `ATE`, or `accuracy` are adjacent to the numeric value.

### 4. Reference Management
- **DON'T** use default author strings directly in LaTeX/BibTeX without cleaning. Semicolons and special characters will break compiler engines.
- **DON'T** forget to escape special characters like `&` (e.g., `IEEE/RSJ Conference on Intelligent Robots & Systems` -> `Intelligent Robots \& Systems`) in BibTeX files.
