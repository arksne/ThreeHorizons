"""Читаем настоящую ошибку Gradio Space через очередь (fn_index + /queue/join)."""
import json
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

HOST = "stabilityai-stable-fast-3d.hf.space"
API_NAME = "/run_button"
IMG = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\ARK\Documents\deepseek-harness\default-workspace\ThreeHorizons\tools\i2m\.tmp\axe_demo.png"
BASE = f"https://{HOST}"
UA = {"User-Agent": "Mozilla/5.0"}


def http(url, payload=None, raw_body=None, headers=None):
    h = dict(UA)
    if headers:
        h.update(headers)
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        h["Content-Type"] = "application/json"
    if raw_body is not None:
        data = raw_body
    req = urllib.request.Request(url, data=data, headers=h, method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8", "replace")


info = json.loads(http(f"{BASE}/info"))
fn_index = None
for i, dep in enumerate(info.get("dependencies", [])):
    if dep.get("api_name") == API_NAME:
        fn_index = i
        break
if fn_index is None:
    for i, dep in enumerate(info.get("dependencies", [])):
        ids = dep.get("inputs", [])
        if ids:
            pass
print("fn_index:", fn_index)

# upload
boundary = "----oc" + str(int(time.time() * 1000))
with open(IMG, "rb") as f:
    img = f.read()
body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; filename=\"in.png\"\r\n"
        "Content-Type: image/png\r\n\r\n").encode() + img + f"\r\n--{boundary}--\r\n".encode()
up = json.loads(http(f"{BASE}/upload/file", raw_body=body,
                     headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}))
print("upload:", up)

session = str(int(time.time() * 1000))
data = [up, 0.3, "None", 10000, 1024]
res = json.loads(http(f"{BASE}/queue/join",
                      {"data": data, "event_data": None, "fn_index": fn_index,
                       "trigger_id": 1, "session_hash": session}))
print("join:", res)

for _ in range(90):
    raw = http(f"{BASE}/queue/data?session_hash={urllib.parse.quote(session)}")
    try:
        d = json.loads(raw)
    except Exception:
        print(raw[:500]); time.sleep(5); continue
    msgs = d.get("messages", [])
    for m in msgs:
        if m.get("msg") == "process_completed":
            print("ERROR:", json.dumps(m.get("output"), ensure_ascii=False)[:2000])
            raise SystemExit(0)
        if m.get("msg") == "estimation" or m.get("msg") == "process_starts":
            print("msg:", m.get("msg"), json.dumps(m.get("output"), ensure_ascii=False)[:300])
    time.sleep(5)
print("no completion in time")
