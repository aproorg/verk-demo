"""PreToolUse hook: block `git commit` and `git push` while on main.

Reads the tool call as JSON on stdin. Exit code 2 blocks the call and
sends stderr back to Claude.
"""

import json
import subprocess
import sys

command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
if "git commit" in command or "git push" in command:
    branch = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    ).stdout.strip()
    if branch == "main":
        print("Ekki commita eða pusha á main. Búðu til grein: git switch -c <númer>-<lýsing>", file=sys.stderr)
        sys.exit(2)
