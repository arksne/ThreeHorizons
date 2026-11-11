"""Reconcile Higgsfield generations with the local reference folders.

Some generations are created server-side even when the submit call reports an
error, so this walks the account's generation list and downloads every render
that matches one of the pipeline prompts into ART_ASSETS/refs/<id>.png.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import hf_mcp as H  # noqa: E402
import prompts as P  # noqa: E402
from run_refgen import MISSING, SUBJECTS, REFS, download, log  # noqa: E402


def build_prompt_map():
    missing = json.load(open(MISSING, encoding="utf-8"))
    subjects = json.load(open(SUBJECTS, encoding="utf-8"))
    by_prompt = {}
    for group, items in missing.items():
        for entry in items:
            cid = entry[0] if isinstance(entry, list) else entry
            sub = subjects.get(cid)
            if not sub:
                continue
            by_prompt[P.build_prompt(group, cid, sub["subject"], sub.get("notes", ""))] = cid
    return by_prompt


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    pmap = build_prompt_map()
    H.initialize()
    H.notifications_initialized()
    got = 0
    for page in range(6):
        data = H.data_of(H.call_tool("show_generations", {"limit": limit}))
        items = data.get("items", []) or []
        if not items:
            break
        for it in items:
            if it.get("status") != "completed":
                continue
            pr = (it.get("params") or {}).get("prompt", "")
            cid = pmap.get(pr)
            if not cid:
                continue
            target = os.path.join(REFS, cid + ".png")
            if os.path.exists(target):
                continue
            res = it.get("results") or {}
            url = res.get("rawUrl") or res.get("url") or ""
            if not url:
                continue
            try:
                size = download(url, target)
                got += 1
                log(f"RECOVERED {cid} <- {it.get('id','')[:8]} ({size} bytes)")
            except Exception as e:
                log(f"RECOVER-FAIL {cid}: {str(e)[:120]}")
        break
    log(f"recovered {got} reference(s)")


if __name__ == "__main__":
    main()
