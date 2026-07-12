#!/usr/bin/env python3
"""
run_all.py — Master orchestrator for the GNSS-Denied Localization SLR Pipeline.

Runs all analysis scripts in the correct order:
  1. 01_clean_data.py       — Data cleaning and preparation
  2. 02_classify_papers.py  — Keyword-based classification
  3. 03_generate_figures.py — Statistical analysis and figures
  4. 04_extract_accuracy.py — Accuracy extraction from abstracts
  5. 05_build_references.py — Bibliography and BibTeX generation
  6. 06_write_report.py     — Analysis report generation

Usage:
    python run_all.py           # Run all steps
    python run_all.py --from 3  # Resume from step 3
    python run_all.py --only 2  # Run only step 2
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Fix Windows console encoding for Unicode output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent

STEPS = [
    ("01_clean_data.py",       "Phase 1: Data Cleaning & Preparation"),
    ("02_classify_papers.py",  "Phase 2: Paper Classification"),
    ("03_generate_figures.py", "Phase 3: Figure Generation & Statistical Analysis"),
    ("04_extract_accuracy.py", "Phase 3b: Accuracy Extraction"),
    ("05_build_references.py", "Phase 4: Bibliography & Reference Building"),
    ("06_write_report.py",     "Phase 5: Analysis Report Generation"),
]


def run_step(script_name: str, description: str, step_num: int) -> bool:
    """Run a single pipeline step and return True if successful."""
    script_path = SCRIPT_DIR / script_name

    if not script_path.exists():
        print(f"  ⚠️  Script not found: {script_path}")
        print(f"  ⚠️  Skipping step {step_num}.")
        return False

    print(f"\n{'='*70}")
    print(f"  Step {step_num}/{len(STEPS)}: {description}")
    print(f"  Script: {script_name}")
    print(f"{'='*70}\n")

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(SCRIPT_DIR),
            capture_output=False,
            text=True,
        )
        elapsed = time.time() - start_time

        if result.returncode == 0:
            print(f"\n  ✅ Step {step_num} completed successfully in {elapsed:.1f}s")
            return True
        else:
            print(f"\n  ❌ Step {step_num} failed with return code {result.returncode}")
            return False

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n  ❌ Step {step_num} failed with error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run the SLR analysis pipeline")
    parser.add_argument("--from", type=int, dest="from_step", default=1,
                        help="Start from this step number (1-6)")
    parser.add_argument("--only", type=int, default=None,
                        help="Run only this step number")
    args = parser.parse_args()

    print("=" * 70)
    print("  🎯 GNSS-Denied Localization — Systematic Literature Review Pipeline")
    print("=" * 70)

    total_start = time.time()
    results = []

    if args.only:
        # Run a single step
        if 1 <= args.only <= len(STEPS):
            script_name, description = STEPS[args.only - 1]
            success = run_step(script_name, description, args.only)
            results.append((args.only, description, success))
        else:
            print(f"  ❌ Invalid step number: {args.only}. Must be 1-{len(STEPS)}")
            sys.exit(1)
    else:
        # Run all steps from the specified starting point
        for i, (script_name, description) in enumerate(STEPS, start=1):
            if i < args.from_step:
                continue
            success = run_step(script_name, description, i)
            results.append((i, description, success))
            if not success:
                print(f"\n  ⚠️  Pipeline paused at step {i}. Fix the issue and re-run.")
                print(f"  💡 To resume: python run_all.py --from {i}")
                break

    total_elapsed = time.time() - total_start

    # Print summary
    print(f"\n\n{'='*70}")
    print(f"  📊 Pipeline Summary")
    print(f"{'='*70}")
    for step_num, desc, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} Step {step_num}: {desc}")
    print(f"\n  Total time: {total_elapsed:.1f}s")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
