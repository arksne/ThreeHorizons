"""Minimal MCP client for the Higgsfield MCP server (streamable HTTP).

Used by the Three Horizons reference-generation pipeline. Handles OAuth token
refresh, JSON-RPC calls and SSE-framed responses.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".higgsfield-mcp-token.json")
AS = "https://clerk.higgsfield.ai"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
RESOURCE = "https://mcp.higgsfield.ai/mcp"


class HiggsfieldError(RuntimeError):
    pass


def _load():
    with open(TOKEN_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)


def access_token(force_refresh=False):
    tok = _load()
    if force_refresh or tok.get("expires_at", 0) < _now() + 120:
        _refresh(tok)
    return tok["access_token"]


def _now():
    import time
    return int(time.time())


def _refresh(tok):
    fields = {
        "grant_type": "refresh_token",
        "refresh_token": tok["refresh_token"],
        "client_id": tok["client_id"],
        "resource": RESOURCE,
    }
    body = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(
        AS + "/oauth/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json", "User-Agent": UA},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        raise HiggsfieldError("token refresh failed: %s %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    data["client_id"] = tok["client_id"]
    data["mcp_url"] = tok.get("mcp_url", RESOURCE)
    data["expires_at"] = _now() + int(data.get("expires_in", 86400))
    _save(data)


def _rpc(method, params, _id=1, notification=False, timeout=180, retries=4):
    payload = {"jsonrpc": "2.0", "method": method}
    if not notification:
        payload["id"] = _id
    if params is not None:
        payload["params"] = params
    body = json.dumps(payload).encode()
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(
            RESOURCE,
            data=body,
            headers={
                "Authorization": "Bearer " + access_token(),
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "User-Agent": UA,
                "MCP-Protocol-Version": "2025-06-18",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                ctype = r.headers.get("Content-Type", "")
                raw = r.read().decode("utf-8", "replace")
            if notification:
                return None
            if "text/event-stream" in ctype:
                for line in raw.splitlines():
                    line = line.strip()
                    if line.startswith("data:"):
                        chunk = line[5:].strip()
                        if chunk:
                            return json.loads(chunk)
                raise HiggsfieldError("no data frame in SSE response: %s" % raw[:400])
            return json.loads(raw)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (401, 403, 400, 404, 429):
                # 401 -> refresh the token once and retry
                if e.code == 401 and attempt == 0:
                    access_token(force_refresh=True)
                    continue
                raise HiggsfieldError("HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, json.JSONDecodeError) as e:
            last = e
        import time as _t
        _t.sleep(min(2 ** attempt * 3, 20))
    raise HiggsfieldError("rpc %s failed: %s" % (method, last))


def initialize():
    # clientInfo.name must be "chatgpt": Higgsfield grants the free-trial
    # unlimited allowance only to the ChatGPT / Claude / Cowork clients.
    return _rpc("initialize", {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "chatgpt", "version": "1.0"},
    })


def notifications_initialized():
    try:
        _rpc("notifications/initialized", {}, notification=True)
    except Exception:
        pass


def list_tools():
    res = _rpc("tools/list", {})
    return res.get("result", {}).get("tools", [])


def call_tool(name, args, timeout=300):
    res = _rpc("tools/call", {"name": name, "arguments": args}, _id=_next_id(), timeout=timeout)
    if "error" in res:
        raise HiggsfieldError(json.dumps(res["error"], ensure_ascii=False)[:600])
    return res.get("result", {})


_ID = [1000]


def _next_id():
    _ID[0] += 1
    return _ID[0]


def text_of(result):
    """Flatten an MCP tool result into plain text."""
    out = []
    for block in result.get("content", []) or []:
        if block.get("type") == "text":
            out.append(block.get("text", ""))
    return "\n".join(out)


def data_of(result):
    """Return parsed structured content of a tool result, if any."""
    if result.get("structuredContent"):
        return result["structuredContent"]
    txt = text_of(result)
    try:
        return json.loads(txt)
    except Exception:
        return {"_text": txt}
