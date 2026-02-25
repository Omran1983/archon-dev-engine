#!/usr/bin/env python3
"""
ARCHON Traffic Monitor
=======================
Polls GitHub traffic API and appends results to a CSV log.
Run daily via Windows Task Scheduler or manually.

Usage:
    python scripts/monitor_traffic.py

Schedule (Windows Task Scheduler):
    Action: python C:\path\to\archon-dev-engine\scripts\monitor_traffic.py
    Trigger: Daily at 09:00
"""

import os
import csv
import json
import datetime
import subprocess

REPO     = "Omran1983/archon-dev-engine"
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "traffic_log.csv")
FIELDNAMES = [
    "date", "clones_total", "clones_unique",
    "views_total", "views_unique",
    "stars", "forks",
    "top_referrer", "top_referrer_count"
]

def gh_api(endpoint: str) -> dict:
    """Call GitHub CLI api."""
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/{endpoint}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[WARN] gh api {endpoint} failed: {result.stderr.strip()}")
        return {}
    return json.loads(result.stdout)

def gh_repo_stats() -> dict:
    result = subprocess.run(
        ["gh", "repo", "view", REPO, "--json",
         "stargazerCount,forkCount"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return {}
    return json.loads(result.stdout)

def latest_file_exists() -> bool:
    return os.path.exists(LOG_FILE)

def append_row(row: dict):
    write_header = not latest_file_exists()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

def run():
    today = datetime.date.today().isoformat()
    print(f"[ARCHON MONITOR] Polling traffic for {REPO} on {today}...")

    clones    = gh_api("traffic/clones")
    views     = gh_api("traffic/views")
    referrers = gh_api("traffic/popular/referrers")
    stats     = gh_repo_stats()

    # Clones: sum last 14 days
    clone_data   = clones.get("clones", [])
    clone_total  = sum(c.get("count", 0) for c in clone_data)
    clone_unique = sum(c.get("uniques", 0) for c in clone_data)

    # Views
    view_data    = views.get("views", [])
    view_total   = sum(v.get("count", 0) for v in view_data)
    view_unique  = sum(v.get("uniques", 0) for v in view_data)

    # Top referrer
    top_ref       = referrers[0] if referrers else {}
    top_ref_name  = top_ref.get("referrer", "none")
    top_ref_count = top_ref.get("count", 0)

    row = {
        "date":              today,
        "clones_total":      clone_total,
        "clones_unique":     clone_unique,
        "views_total":       view_total,
        "views_unique":      view_unique,
        "stars":             stats.get("stargazerCount", 0),
        "forks":             stats.get("forkCount", 0),
        "top_referrer":      top_ref_name,
        "top_referrer_count": top_ref_count,
    }

    append_row(row)

    print(f"  Clones (14d): {clone_total} total / {clone_unique} unique")
    print(f"  Views  (14d): {view_total} total / {view_unique} unique")
    print(f"  Stars: {row['stars']}  |  Forks: {row['forks']}")
    print(f"  Top referrer: {top_ref_name} ({top_ref_count} hits)")
    print(f"  Logged to: {os.path.abspath(LOG_FILE)}")

if __name__ == "__main__":
    run()
