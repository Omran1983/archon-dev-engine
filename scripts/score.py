#!/usr/bin/env python3
import os
import sys

def score_file(filepath):
    if not os.path.isfile(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    scores = {
        "async": 0,
        "structured": 0,
        "config": 0,
        "logging": 0
    }
    
    # 1. Async Compliance
    if "async " in content or "await " in content:
        scores["async"] = 100
    elif any(kw in content for kw in ["requests.", "urllib.", "sleep("]):
        scores["async"] = 0 # Major penalty
    else:
        scores["async"] = 100 # Default to pass if no I/O detected

    # 2. Structured Output
    if "json.dumps" in content or "pydantic" in content or "Zod" in content:
        scores["structured"] = 100
    elif "print(" in content:
        scores["structured"] = 50
    else:
        scores["structured"] = 100

    # 3. Config Discipline
    if "os.getenv" in content or "environ" in content:
        scores["config"] = 100
    elif any(kw in content for kw in ["api_key =", "secret =", "password ="]):
        scores["config"] = 0
    else:
        scores["config"] = 80

    return scores

def run_scorer():
    print("--- ARCHON Architecture Score ---")
    files = [f for f in os.listdir('.') if f.endswith('.py') or f.endswith('.ts') or f.endswith('.js')]
    
    if not files:
        print("No source files found to score.")
        return

    total_stats = {"async": [], "structured": [], "config": []}
    
    for f in files:
        res = score_file(f)
        if res:
            for k in total_stats:
                total_stats[k].append(res[k])

    avg_async = sum(total_stats["async"]) / len(total_stats["async"])
    avg_struct = sum(total_stats["structured"]) / len(total_stats["structured"])
    avg_cfg = sum(total_stats["config"]) / len(total_stats["config"])
    
    overall = (avg_async + avg_struct + avg_cfg) / 3
    
    print(f"Overall Quality: {overall:.1f}%")
    print(f"  > Async-First Compliance: {avg_async:.1f}%")
    print(f"  > Structured Discipline: {avg_struct:.1f}%")
    print(f"  > Configuration Integrity: {avg_cfg:.1f}%")
    print("-" * 33)
    
    if overall > 90:
        print("Status: ELITE (Production Ready)")
    elif overall > 70:
        print("Status: STABLE (Ready for Review)")
    else:
        print("Status: FRAGILE (Immediate Refactor Recommended)")

if __name__ == "__main__":
    run_scorer()
