# -*- coding: utf-8 -*-
"""Клиент MCP-сервера Higgsfield AI (https://mcp.higgsfield.ai/mcp).

Тонкая обёртка над JSON-RPC по HTTP: initialize → tools/call → ждём job → скачиваем файлы.
Авторизация — OAuth-токен из hf_token.json (обновляется refresh_token'ом).

Использование:
    python -X utf8 tools/higgsfield.py list-tools
    python -X utf8 tools/higgsfield.py call <tool> '<json-args>'
    python -X utf8 tools/higgsfield.py schema <tool>
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN_FILE = ROOT.parent / "_git_cleanup" / "hf_token.json"
URL = "https://mcp.higgsfield.ai/mcp"
RESOURCE = "https://mcp.higgsfield.ai/mcp"
AUTH = "https://mcp.higgsfield.ai"

_session_id = None


def token() -> dict:
    p = Path(os.environ.get("HF_TOKEN_FILE", TOKEN_FILE))
    if not p.exists():
        raise SystemExit(f"нет файла токена: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def refresh() -> dict:
    """Обновляет access_token по refresh_token."""
    t = token()
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": t["refresh_token"],
        "client_id": t["client_id"],
        "scope": "openid email offline_access",
        "resource": RESOURCE,
    }).encode()
    req = urllib.request.Request(f"{AUTH}/oauth2/token", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            new = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"refresh не удался: HTTP {e.code} {body[:300]}")
    p = Path(os.environ.get("HF_TOKEN_FILE", TOKEN_FILE))
    p.write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding="utf-8")
    return new


def rpc(method: str, params: dict, _retry: bool = True) -> dict:
    global _session_id
    t = token()
    headers = {
        "Authorization": f"Bearer {t['access_token']}",
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    if _session_id:
        headers["Mcp-Session-Id"] = _session_id
    body = json.dumps({"jsonrpc": "2.0", "id": int(time.time() * 1000) % 10**9,
                       "method": method, "params": params}).encode()
    req = urllib.request.Request(URL, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            sid = r.headers.get("Mcp-Session-Id")
            if sid:
                _session_id = sid
            raw = r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 401 and _retry:
            refresh()
            return rpc(method, params, _retry=False)
        body = e.read().decode(errors="replace")
        raise SystemExit(f"HTTP {e.code}: {body[:600]}")
    # SSE: собираем data-строки
    out = []
    for line in raw.splitlines():
        if line.startswith("data: "):
            out.append(line[6:])
    for line in raw.splitlines():
        if line.startswith("{") and not out:
            out.append(line)
    if not out:
        return {"raw": raw[:2000]}
    return json.loads(out[-1])


def init():
    r = rpc("initialize", {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "three-horizons-refs", "version": "1.0"},
    })
    # уведомление «initialized»
    global _session_id
    t = token()
    headers = {"Authorization": f"Bearer {t['access_token']}",
               "Accept": "application/json, text/event-stream",
               "Content-Type": "application/json"}
    if _session_id:
        headers["Mcp-Session-Id"] = _session_id
    body = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(URL, data=body, method="POST",
                                                      headers=headers), timeout=30)
    except Exception:
        pass
    return r


def call(tool: str, args: dict, _init: bool = False) -> dict:
    if _init:
        init()
    return rpc("tools/call", {"name": tool, "arguments": args})


def text_of(resp: dict) -> str:
    """Достаёт текст из ответа tools/call."""
    res = resp.get("result", resp)
    if isinstance(res, dict) and "content" in res:
        parts = []
        for c in res["content"]:
            if isinstance(c, dict):
                if c.get("type") == "text":
                    parts.append(c.get("text", ""))
                elif "json" in c:
                    parts.append(json.dumps(c["json"], ensure_ascii=False, indent=1))
        return "\n".join(parts)
    return json.dumps(res, ensure_ascii=False, indent=1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "list-tools":
        r = init()
        r = rpc("tools/list", {})
        tools = r.get("result", {}).get("tools", [])
        for t in tools:
            print(f"  {t['name']}")
        print(f"\nвсего: {len(tools)}")
    elif cmd == "schema":
        tool = sys.argv[2]
        r = rpc("tools/list", {})
        for t in r.get("result", {}).get("tools", []):
            if t["name"] == tool:
                print(json.dumps(t.get("inputSchema", {}), ensure_ascii=False, indent=1))
                return
        print("не найден")
    elif cmd == "call":
        tool = sys.argv[2]
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        r = call(tool, args, _init=True)
        print(text_of(r))
    elif cmd == "init":
        print(json.dumps(init(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
