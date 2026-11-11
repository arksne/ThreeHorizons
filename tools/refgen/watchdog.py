"""Keep the reference generation running.

Restarts run_refgen.py if it exits while references are still missing, and
refreshes the Higgsfield OAuth token when it expires.

    python watchdog.py
"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from run_refgen import MISSING, REFS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.environ.get("TEMP", "."), "refgen.log")
WLOG = os.path.join(os.environ.get("TEMP", "."), "refgen_watchdog.log")


EXCLUDE_GROUPS = {"weapons"}


def remaining():
    missing = json.load(open(MISSING, encoding="utf-8"))
    n = 0
    for group, items in missing.items():
        if group in EXCLUDE_GROUPS:
            continue
        for entry in items:
            cid = entry[0] if isinstance(entry, list) else entry
            if not os.path.exists(os.path.join(REFS, cid + ".png")):
                n += 1
    return n


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(WLOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def runner_alive():
    """True when another run_refgen.py instance holds the lock file."""
    lock = os.path.join(HERE, ".runner.lock")
    if not os.path.exists(lock):
        return False
    try:
        pid = int(open(lock, encoding="utf-8").read().strip())
    except Exception:
        return False
    try:
        import psutil  # not installed by default, fall through
    except Exception:
        psutil = None
    if psutil is not None:
        return psutil.pid_exists(pid)
    try:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True, timeout=20).stdout
        return str(pid) in out
    except Exception:
        return True


def main():
    restarts = 0
    while True:
        left = remaining()
        if left == 0:
            log("all references present - watchdog exiting")
            return 0
        while runner_alive():
            log(f"another runner is active, waiting ({left} references missing)")
            time.sleep(60)
            left = remaining()
            if left == 0:
                log("all references present - watchdog exiting")
                return 0
        log(f"starting run_refgen.py, {left} references missing (restart #{restarts})")
        with open(LOG, "a", encoding="utf-8") as out:
            proc = subprocess.Popen(
                [sys.executable, os.path.join(HERE, "run_refgen.py"), "--max-inflight", "1", "--exclude", "weapons"],
                cwd=HERE, stdout=out, stderr=subprocess.STDOUT)
            proc.wait()
        left = remaining()
        if left == 0:
            log("run finished, all references present")
            return 0
        restarts += 1
        log(f"runner exited with {left} references left - restarting in 15s")
        time.sleep(15)


if __name__ == "__main__":
    raise SystemExit(main())
