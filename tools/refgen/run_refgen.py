"""Generate the missing Three Horizons reference images through the Higgsfield MCP.

Usage:
    python run_refgen.py --groups weapons,details --max-inflight 1
    python run_refgen.py --dry-run --groups tiles

The run is idempotent: a reference whose PNG already exists is skipped.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import hf_mcp as H  # noqa: E402
import prompts as P  # noqa: E402

ROOT = r"C:\Users\ARK\Documents\deepseek-harness\default-workspace\ThreeHorizons"
REFS = os.path.join(ROOT, "ART_ASSETS", "refs")
MISSING = os.path.join(ROOT, "tools", "refgen", "missing.json")
SUBJECTS = os.path.join(ROOT, "tools", "refgen", "subjects.json")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


GROUP_ORDER = ["ships", "details", "items", "tools", "tiles", "ui", "weather", "weapons"]


def load_work(groups, only=None, skip_existing=True, exclude=None):
    missing = json.load(open(MISSING, encoding="utf-8"))
    subjects = json.load(open(SUBJECTS, encoding="utf-8"))
    work = []
    ordered = [g for g in GROUP_ORDER if g in missing] + [g for g in missing if g not in GROUP_ORDER]
    for group in ordered:
        items = missing[group]
        if groups and group not in groups:
            continue
        if exclude and group in exclude:
            continue
        for entry in items:
            cid = entry[0] if isinstance(entry, list) else entry
            if only and cid not in only:
                continue
            target = os.path.join(REFS, cid + ".png")
            if skip_existing and os.path.exists(target):
                continue
            sub = subjects.get(cid)
            if not sub:
                log(f"SKIP {cid}: no subject description")
                continue
            prompt = P.build_prompt(group, cid, sub["subject"], sub.get("notes", ""))
            work.append({"id": cid, "group": group, "prompt": prompt,
                         "aspect": P.aspect_for(group, cid), "target": target})
    return work


def download(url, path):
    """Download to a temp file and rename, so a failed transfer never leaves a
    half-written PNG that a later run would treat as finished."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    if len(data) < 2000:
        raise IOError(f"downloaded too little ({len(data)} bytes)")
    tmp = path + ".part"
    try:
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return len(data)


def submit(item, model, resolution):
    params = {
        "model": model,
        "prompt": item["prompt"],
        "aspect_ratio": item["aspect"],
        "use_unlim": True,
    }
    if resolution:
        params["resolution"] = resolution
    res = H.call_tool("generate_image", {"params": params}, timeout=180)
    data = H.data_of(res)
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(data["error"])
    if isinstance(data, dict) and data.get("results"):
        r0 = data["results"][0]
        # Higgsfield returns the job id as "id" for generate_image and as
        # "job_id" for generate_image_batch.
        job_id = r0.get("job_id") or r0.get("id")
        if r0.get("status") == "submission_failed" or not job_id:
            raise RuntimeError(r0.get("error") or "submission_failed")
        return job_id
    raise RuntimeError("unexpected submit payload: " + json.dumps(data, ensure_ascii=False)[:300])


def adopt_orphan(item, known):
    """Higgsfield sometimes reports a submission error while the job was in fact
    created. Look for a fresh job with the same prompt and adopt it."""
    try:
        data = H.data_of(H.call_tool("show_generations", {"limit": 6}))
    except Exception:
        return None
    for it in data.get("items", []) or []:
        jid = it.get("id")
        pr = (it.get("params") or {}).get("prompt", "")
        if jid and jid not in known and pr == item["prompt"]:
            return jid
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", default="")
    ap.add_argument("--exclude", default="")
    ap.add_argument("--only", default="")
    ap.add_argument("--model", default="seedream_v5_pro")
    ap.add_argument("--resolution", default="2k")
    ap.add_argument("--max-inflight", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    lock = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".runner.lock")
    with open(lock, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    try:
        return _run(args)
    finally:
        try:
            if open(lock, encoding="utf-8").read().strip() == str(os.getpid()):
                os.remove(lock)
        except Exception:
            pass


def _run(args):
    groups = [g.strip() for g in args.groups.split(",") if g.strip()]
    exclude = [g.strip() for g in args.exclude.split(",") if g.strip()]
    only = [i.strip() for i in args.only.split(",") if i.strip()]
    work = load_work(groups, only, exclude=exclude)
    if args.limit:
        work = work[: args.limit]
    log(f"work items: {len(work)} (model={args.model} res={args.resolution} inflight={args.max_inflight})")
    if args.dry_run:
        for w in work:
            print("=" * 80)
            print(w["id"], "|", w["group"], "|", w["aspect"])
            print(w["prompt"])
        return 0

    H.initialize()
    H.notifications_initialized()

    queue = list(work)
    inflight = {}
    attempts = {}
    known_jobs = set()
    done = 0
    failed = []
    backoff = 45
    last_submit_ok = 0.0

    while queue or inflight:
        # --- submit ---
        while queue and len(inflight) < args.max_inflight:
            item = queue[0]
            try:
                job_id = submit(item, args.model, args.resolution)
                inflight[job_id] = item
                known_jobs.add(job_id)
                queue.pop(0)
                backoff = 45
                last_submit_ok = time.time()
                log(f"SUBMIT {item['id']} -> {job_id[:8]} ({len(queue)} queued, {len(inflight)} inflight)")
            except Exception as e:
                msg = str(e)
                orphan = adopt_orphan(item, known_jobs)
                if orphan:
                    inflight[orphan] = item
                    known_jobs.add(orphan)
                    queue.pop(0)
                    backoff = 45
                    log(f"SUBMIT-RECOVERED {item['id']} -> {orphan[:8]} (server reported: {msg[:80]})")
                    continue
                wait = backoff
                if "rate" in msg.lower() or "429" in msg or "concurrent" in msg.lower():
                    wait = max(backoff, 60)
                backoff = min(int(backoff * 1.5), 300)
                log(f"SUBMIT-FAIL {item['id']}: {msg[:140]} (retry in {wait}s)")
                time.sleep(wait)
                break  # retry the same item on the next round

        if not inflight:
            continue

        # --- poll ---
        jobs = [{"index": i, "job_id": jid} for i, (jid, _) in enumerate(inflight.items())]
        try:
            res = H.data_of(H.call_tool("jobs_wait", {"jobs": jobs, "timeout_seconds": 15}, timeout=90))
        except Exception as e:
            log(f"POLL-ERROR: {str(e)[:160]}")
            time.sleep(10)
            continue
        for jr in res.get("jobs", []):
            jid = jr.get("job_id")
            item = inflight.get(jid)
            if item is None:
                continue
            status = jr.get("status")
            if status in ("completed", "failed", "error", "canceled"):
                url = jr.get("result_url") or ""
                if status == "completed" and url:
                    try:
                        size = download(url, item["target"])
                        done += 1
                        log(f"DONE {item['id']} -> {item['target']} ({size} bytes)")
                    except Exception as e:
                        log(f"DOWNLOAD-FAIL {item['id']}: {str(e)[:160]}")
                        failed.append(item["id"])
                else:
                    log(f"FAILED {item['id']}: {status} {json.dumps(jr, ensure_ascii=False)[:200]}")
                    failed.append(item["id"])
                    attempts[item["id"]] = attempts.get(item["id"], 0) + 1
                    if attempts[item["id"]] < 4:
                        queue.insert(0, item)  # retry later
                inflight.pop(jid, None)
        time.sleep(1)

    log(f"FINISHED done={done} failed={len(failed)}")
    if failed:
        log("failed ids: " + ", ".join(failed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
