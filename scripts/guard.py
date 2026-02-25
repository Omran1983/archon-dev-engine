#!/usr/bin/env python3
import sys
import os

def check_architecture(filepath):
    """Enforces ARCHON Async-First & Deterministic Doctrine."""
    if not os.path.exists(filepath):
        print(f"[ERR] File not found: {filepath}")
        return False
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERR] Could not read {filepath}: {e}")
        return True # Skip files that can't be read (binary etc)

    # DOCTRINE 1: Async-First for I/O
    # Detecting blocking I/O calls in files that don't have 'async'
    io_keywords = ["requests.get(", "requests.post(", "http.client", "urllib.request"]
    if any(kw in content for kw in io_keywords) and "async " not in content:
        print(f"[ARCHON VETO] {os.path.basename(filepath)}: Blocking I/O detected without 'async'. Doctrine Violation.")
        return False
        
    # DOCTRINE 2: Deterministic Patterns
    # Preventing bare prints in non-main logic
    if "print(" in content and "__name__ == \"__main__\"" not in content and ".py" in filepath:
         print(f"[ARCHON WARN] {os.path.basename(filepath)}: Bare 'print' used in module logic. Recommend structured logging.")

    return True

def main():
    files_to_check = sys.argv[1:]
    if not files_to_check:
        return 0

    vetoes = 0
    for filepath in files_to_check:
        if not check_architecture(filepath):
            vetoes += 1

    if vetoes > 0:
        print(f"\n[ARCHON GUARD] Commit aborted. {vetoes} architecture violations found.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
