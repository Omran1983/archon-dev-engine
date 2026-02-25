#!/usr/bin/env python3
import sys
import os
import re

def check_architecture(filepath):
    """Enforces ARCHON Async-First & Deterministic Doctrine."""
    # Skip binary and non-source files
    BINARY_EXTS = {'.gif', '.png', '.jpg', '.jpeg', '.pdf', '.zip', '.exe', '.pyc'}
    SOURCE_EXTS = {'.py', '.ts', '.js', '.jsx', '.tsx'}
    ext = os.path.splitext(filepath)[1].lower()
    if ext in BINARY_EXTS or ext not in SOURCE_EXTS:
        return True

    if not os.path.exists(filepath):
        return True

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return True  # Skip unreadable/binary content
    except Exception as e:
        print(f"[WARN] Could not read {filepath}: {e}")
        return True

    # DOCTRINE 1: Async-First
    # Match actual blocking I/O calls — not string literals or comments
    io_pattern = re.compile(
        r'^\s*(?!#).*\b(requests\.get|requests\.post|http\.client|urllib\.request)\s*\(',
        re.MULTILINE
    )
    if io_pattern.search(content) and "async " not in content:
        print(f"[ARCHON VETO] {os.path.basename(filepath)}: Blocking I/O detected without 'async'. Doctrine Violation.")
        return False

    # DOCTRINE 2: Structured Output
    if "print(" in content and "__name__ == \"__main__\"" not in content and ext == '.py':
        print(f"[ARCHON WARN] {os.path.basename(filepath)}: Bare 'print' in module. Recommend structured logging.")

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
