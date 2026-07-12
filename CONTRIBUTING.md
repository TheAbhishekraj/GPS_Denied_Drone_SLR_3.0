# Contributing to GPS_Denied_Drone_SLR_3.0

Thank you for your interest in contributing to this open-science systematic literature review! We welcome contributions to improve the parsing rules, expand the classification taxonomies, or enhance the visualization outputs.

---

## 📋 Code of Conduct
By participating in this project, you agree to abide by standard academic integrity principles and maintain a respectful, collaborative environment.

---

## 🛠️ How to Contribute

### 1. Reporting Issues
If you identify inaccuracies in paper classifications, bugs in the regex parsing logic, or visual bugs in figure generation:
- Search the existing issues to ensure it hasn't already been reported.
- Open a new issue with a clear description, reproduction steps, and expected behavior.

### 2. Proposing Taxonomy Enhancements
If you wish to add new keywords or modify classification criteria:
1.  Fork the repository.
2.  Edit the classification dictionaries in `analysis/scripts/02_classify_papers.py`.
3.  Run the pipeline check (`python analysis/scripts/run_all.py`) to verify that the classification operates correctly without breaking existing pipeline stages.
4.  Commit your changes and open a Pull Request.

---

## 📝 Coding Standards

- **Relative Paths:** Do not use absolute paths (e.g. `C:\Users\...`). Always navigate from the project root using `pathlib.Path(__file__)`.
- **Windows Console Encoding:** All python scripts outputting console print logs with Unicode characters must reconfigure the console:
  ```python
  import sys
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  ```
- **Fenced Dictionaries:** Ensure all added regex boundaries use `\b` to prevent partial substring matches.
