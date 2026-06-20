#!/usr/bin/env python3
"""Generate job search report from search results."""
import json, os
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
results_file = os.path.join(output_dir, "job_search_results.csv")
if os.path.exists(results_file):
    print(f"Report file exists: {results_file}")
else:
    print("No search results found. Run search first.")
    print(f"Expected at: {results_file}")
