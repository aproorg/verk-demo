"""Run the API and the web app together. One Ctrl+C stops both."""

import signal
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parent.parent
shell = sys.platform == "win32"  # npm is npm.cmd on Windows
procs = [
    subprocess.Popen(["uv", "run", "fastapi", "dev", "app/main.py"], cwd=root / "api", shell=shell),
    subprocess.Popen(["npm", "run", "dev"], cwd=root / "web", shell=shell),
]

try:
    # also ends if one of the two dies on its own, e.g. the port is taken
    while all(p.poll() is None for p in procs):
        time.sleep(0.2)
except KeyboardInterrupt:
    pass

# The terminal sent Ctrl+C to both children as well. Wait for them, and
# insist if one is still up after 3 seconds, so a second Ctrl+C is never needed.
signal.signal(signal.SIGINT, signal.SIG_IGN)
deadline = time.monotonic() + 3
for p in procs:
    if p.poll() is None:
        try:
            p.wait(max(0.1, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            p.terminate()
            try:
                p.wait(2)
            except subprocess.TimeoutExpired:
                p.kill()
