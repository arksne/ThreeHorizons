"""Сырой Gradio-вызов: показывает настоящий текст ошибки (show_error выключен)."""
import json
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

HOST = sys.argv[1] if len(sys.argv) > 1 else "stabilityai-stable-fast-3d.hf.space"
EP = sys.argv[2] if len(sys.argv) > 2 else "run_button"
IMG = sys.argv[3] if len(sys.argv) > 3 else r"C:\Users\ARK\Documents\deepseek-harness\default-workspace\ThreeHorizons\tools\i2m\.tmp\axe_demo.png"
DATA = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None

BASE = f"https://{HOST}/gradio_api"
UA = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}


def get_json(url, payload=None):
    if payload is None:
        req = urllib.request.Request(url, headers=UA)
    else:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={**UA, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")


# 1) грузим файл
with open(IMG, "rb") as f:
    raw = f.read()
up = json.loads(get_json(f"{BASE}/upload/file", {"data": [], "files": []})) if False else None

# простой загрузчик
boundary = "----opencode" + str(int(time.time()))
parts = []
parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; filename=\"input.png\"\r\nContent-Type: image/png\r\n\r\n".encode() + raw + b"\r\n")
parts.append(f"--{boundary}--\r\n".encode())
body = b"".join(parts)
req = urllib.request.Request(f"{BASE}/upload/file", data=body,
                             headers={"User-Agent": "Mozilla/5.0",
                                      "Content-Type": f"multipart/form-data; boundary={boundary}"},
                             method="POST")
with urllib.request.urlopen(req, timeout=300) as r:
    up = json.loads(r.read().decode("utf-8", "replace"))
print("uploaded:", up)

if DATA is None:
    DATA = [up, 0.3, "None", 10000, 1024]
else:
    DATA[0] = up

ev = json.loads(get_json(f"{BASE}/call/{EP}", {"data": DATA}))
print("event_id:", ev)
eid = ev.get("event_id")

for _ in range(120):
    with urllib.request.urlopen(urllib.request.Request(f"{BASE}/call/{EP}/{eid}", headers=UA), timeout=120) as r:
        raw = r.read().decode("utf-8", "replace")
    if '"event_id"' not in raw or '"is_running": false' in raw:
        pass
    if "error" in raw.lower() or "success" in raw.lower():
        print("RAW:", raw[:3000])
        break
    time.sleep(5)
else:
    print("timeout; raw tail:", raw[-2000:])
