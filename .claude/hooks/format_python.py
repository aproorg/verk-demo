"""PostToolUse hook: run ruff format on the Python file Claude just edited."""

import json
import subprocess
import sys

path = json.load(sys.stdin).get("tool_input", {}).get("file_path", "")
if path.endswith(".py"):
    subprocess.run(["ruff", "format", "--quiet", path])
