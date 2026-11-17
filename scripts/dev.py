"""Run the API and the web app together.

One Ctrl+C stops both. Starting it again, from any terminal, first stops
the instance that is already running.
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parent.parent
pidfile = root / ".dev.pid"
windows = sys.platform == "win32"


def stop_previous() -> None:
    try:
        pid = int(pidfile.read_text())
    except (OSError, ValueError):
        return
    if windows:
        # /T takes the whole process tree with it
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], check=False, capture_output=True)
        time.sleep(1)
        return
    # the pid may have been reused by something unrelated since the file was written
    owner = subprocess.run(
        ["ps", "-p", str(pid), "-o", "command="], check=False, capture_output=True, text=True
    )
    if "dev.py" not in owner.stdout:
        return
    print(f"Stopping the dev servers that are already running (pid {pid})")
    os.kill(pid, signal.SIGTERM)
    for _ in range(80):  # it needs up to ~5 s to take its children down
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.1)


def interrupt(*_: object) -> None:
    raise KeyboardInterrupt


stop_previous()
pidfile.write_text(str(os.getpid()))
signal.signal(signal.SIGTERM, interrupt)  # what stop_previous() sends

procs = [
    # shell on Windows because npm is npm.cmd there
    subprocess.Popen(
        ["uv", "run", "fastapi", "dev", "app/main.py"], cwd=root / "api", shell=windows
    ),
    subprocess.Popen(["npm", "run", "dev"], cwd=root / "web", shell=windows),
]

try:
    # also ends if one of the two dies on its own, e.g. the port is taken
    while all(p.poll() is None for p in procs):
        time.sleep(0.2)
except KeyboardInterrupt:
    pass

# Take both down, and insist after 3 seconds, so a second Ctrl+C is never needed.
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
for p in procs:
    if p.poll() is None:
        p.terminate()
deadline = time.monotonic() + 3
for p in procs:
    try:
        p.wait(max(0.1, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        p.kill()

if pidfile.read_text() == str(os.getpid()):
    pidfile.unlink()
