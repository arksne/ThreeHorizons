"""Progress report for the Three Horizons reference generation run.

    python status.py
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from run_refgen import MISSING, REFS  # noqa: E402

LOG = os.path.join(os.environ.get("TEMP", "."), "refgen.log")


def main():
    missing = json.load(open(MISSING, encoding="utf-8"))
    total = sum(len(v) for v in missing.values())
    have = Counter()
    for group, items in missing.items():
        for entry in items:
            cid = entry[0] if isinstance(entry, list) else entry
            if os.path.exists(os.path.join(REFS, cid + ".png")):
                have[group] += 1
    done = sum(have.values())
    print(f"references: {done}/{total} ({done * 100 // max(total, 1)}%)")
    for group in ("weapons", "details", "ships", "items", "tools", "tiles", "ui", "weather"):
        n = len(missing.get(group, []))
        if n:
            print(f"  {group:10} {have[group]:3}/{n:3}")
    if os.path.exists(LOG):
        print("\n--- last log lines ---")
        with open(LOG, encoding="utf-8", errors="replace") as f:
            lines = [l.rstrip() for l in f if l.strip()]
        for line in lines[-8:]:
            print("  " + line)


if __name__ == "__main__":
    main()
