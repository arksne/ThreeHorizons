"""Render the Three Horizons lore/history video through the Higgsfield MCP.

Source: docs/THREE_HORIZONS_PROJECT_BIBLE.md (lore, factions, history).
Model: seedance_2_0 (covered by the free unlimited allowance).

    python make_lore_video.py
"""
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import hf_mcp as H  # noqa: E402

ROOT = r"C:\Users\ARK\Documents\deepseek-harness\default-workspace\ThreeHorizons"
OUT_DIR = os.path.join(ROOT, "ART_ASSETS", "video")
OUT_FILE = os.path.join(OUT_DIR, "three-horizons-lore.mp4")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

PROMPT = (
    "A cinematic establishing montage of a world that lives above the clouds. "
    "Shot 1: slow aerial push over an endless sunlit cloud sea at dawn, three distant island silhouettes on the horizon. "
    "Shot 2: a graphite-grey industrial island city, engineers in leather aprons hauling glowing pale-blue ether fuel drums, "
    "black iron chimneys and stone foundries, smoke drifting sideways in the wind. "
    "Shot 3: a pale limestone trading harbour of another island, merchants loading crates of glowing aquacrystals into a heavy merchant ship, "
    "crowds on the quay and canvas awnings on the market square. "
    "Shot 4: a green farmland island, wheat terraces, granaries, a windmill turning, villagers carrying sacks into a stone barn. "
    "Shot 5: a small neutral harbour town where three ships from three different islands tie up side by side at dawn, "
    "sailors from different factions meeting on the quay, and far in the background a rough pirate anchorage built of wrecked hulls and patched sails. "
    "Shot 6: three figures standing on the quay at sunrise, one in an engineer's blue coat, one in a trader's blue jerkin, one in a green cloak, "
    "looking out over the cloud sea as the camera cranes up and away into the clouds. "
    "Style: stylized realism, medieval maritime, vintage exploration, muted desaturated vintage palette, soft warm shadows, "
    "slight old-film grain, painted maritime-chart feel. No magic, no fantasy creatures, no neon, no modern technology, no cyberpunk, "
    "no text, no captions, no logo, no watermark. Even natural daylight, no harsh contrast. Grounded, human, historical feeling."
)


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=900) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def submit(duration, resolution):
    res = H.call_tool("generate_video", {"params": {
        "model": "seedance_2_0",
        "prompt": PROMPT,
        "aspect_ratio": "16:9",
        "duration": duration,
        "resolution": resolution,
        "generate_audio": True,
        "use_unlim": True,
    }}, timeout=300)
    data = H.data_of(res)
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(data["error"])
    job_id = None
    if isinstance(data, dict):
        if data.get("results"):
            job_id = data["results"][0].get("job_id") or data["results"][0].get("id")
        elif data.get("job_id"):
            job_id = data["job_id"]
    if not job_id:
        raise RuntimeError("no job id: " + json.dumps(data, ensure_ascii=False)[:200])
    return job_id


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    H.initialize()
    H.notifications_initialized()

    job_id = None
    backoff = 60
    for duration, resolution in ((15, "720p"), (10, "720p"), (5, "720p")):
        while True:
            try:
                job_id = submit(duration, resolution)
                log(f"submitted {duration}s {resolution} -> {job_id}")
                break
            except Exception as e:
                msg = str(e)
                if "don't cover this configuration" in msg or "don't cover" in msg:
                    log(f"{duration}s {resolution} not covered by the allowance, trying a shorter cut")
                    break
                log(f"submit failed: {msg[:160]} (retry in {backoff}s)")
                time.sleep(backoff)
                backoff = min(int(backoff * 1.5), 300)
        if job_id:
            break
    if not job_id:
        log("could not submit the video")
        return 1

    for i in range(360):
        r = H.data_of(H.call_tool("jobs_wait", {"jobs": [{"index": 0, "job_id": job_id}], "timeout_seconds": 15}, timeout=90))
        jr = (r.get("jobs") or [{}])[0]
        st = jr.get("status")
        if st in ("completed", "failed", "error", "canceled"):
            log("final: " + json.dumps(jr, ensure_ascii=False)[:400])
            url = jr.get("result_url") or ""
            if st == "completed" and url:
                size = download(url, OUT_FILE)
                log(f"saved {OUT_FILE} ({size} bytes)")
                return 0
            return 3
        if i % 4 == 0:
            log(f"status {st}")
        time.sleep(5)
    log("timeout waiting for the video")
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
