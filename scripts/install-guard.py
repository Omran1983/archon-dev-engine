#!/usr/bin/env python3
import os
import shutil
import sys

def install_guard():
    repo_root = os.popen('git rev-parse --show-toplevel').read().strip()
    if not repo_root:
        print("[ERR] Not a git repository.")
        return

    hooks_dir = os.path.join(repo_root, '.git', 'hooks')
    pre_commit_path = os.path.join(hooks_dir, 'pre-commit')
    
    guard_script_src = os.path.join(os.path.dirname(__file__), 'guard.py')
    guard_script_dest = os.path.join(hooks_dir, 'archon-guard.py')

    # Copy guard logic to .git/hooks
    shutil.copy2(guard_script_src, guard_script_dest)
    print(f"[OK] ARCHON Guard logic copied to {guard_script_dest}")

    # Create pre-commit hook (use forward slashes for path compatibility in sh)
    guard_script_unix = guard_script_dest.replace('\\', '/')
    with open(pre_commit_path, 'w') as f:
        f.write("#!/bin/sh\n")
        f.write(f"python3 \"{guard_script_unix}\" $(git diff --cached --name-only --diff-filter=ACM)\n")
    
    # Make executable
    if os.name != 'nt':
        os.chmod(pre_commit_path, 0o755)
    
    print(f"[OK] Pre-commit hook installed at {pre_commit_path}")
    print("\nARCHON Guard is now Fail-Closed. Any doctrine violations will block commits.")

if __name__ == "__main__":
    install_guard()
