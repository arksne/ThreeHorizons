"""Клиент MCP-сервера Blender (uvx mcp-for-blender) через stdio.

Даёт доступ к живым инструментам Blender: execute_blender_code, look, get_scene_info,
generate_3d, search_assets, import_asset. Сервер подключается к Blender по сокету
127.0.0.1:9876 (см. tools/start_blender_mcp.ps1).

    python tools/blender_mcp_client.py list
    python tools/blender_mcp_client.py code "import bpy; print(bpy.app.version_string)"
    python tools/blender_mcp_client.py look
"""
import json
import os
import subprocess
import sys
import threading
import time

sys.stdout.reconfigure(encoding="utf-8")

UVX = r"C:\Users\ARK\.local\bin\uvx.EXE"
PKG = "mcp-for-blender"
PROTOCOL = "2024-11-05"


class BlenderMCP:
    def __init__(self, exe=UVX, pkg=PKG, cwd=None):
        self.exe = exe
        self.pkg = pkg
        self.cwd = cwd or os.path.dirname(os.path.abspath(__file__))
        self.proc = None
        self._id = 0
        self._lock = threading.Lock()

    # ---------- transport ----------
    def start(self, wait=25):
        self.proc = subprocess.Popen(
            [self.exe, self.pkg],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding="utf-8", bufsize=1, cwd=self.cwd,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        self._send({"jsonrpc": "2.0", "id": self._next(), "method": "initialize",
                    "params": {"protocolVersion": PROTOCOL, "capabilities": {},
                               "clientInfo": {"name": "three-horizons", "version": "1.0"}}})
        deadline = time.time() + wait
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                time.sleep(0.2)
                continue
            try:
                msg = json.loads(line)
            except Exception:
                continue
            if msg.get("id") == 1:
                break
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        return self

    def _next(self):
        with self._lock:
            self._id += 1
            return self._id

    def _send(self, obj):
        self.proc.stdin.write(json.dumps(obj) + "\n")
        self.proc.stdin.flush()

    def _read(self, want_id, timeout=900):
        deadline = time.time() + timeout
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except Exception:
                continue
            if msg.get("id") == want_id:
                return msg
        raise TimeoutError(f"MCP не ответил за {timeout}s")

    # ---------- api ----------
    def call(self, name, args=None, timeout=900):
        i = self._next()
        self._send({"jsonrpc": "2.0", "id": i, "method": "tools/call",
                    "params": {"name": name, "arguments": args or {}}})
        msg = self._read(i, timeout)
        if "error" in msg:
            raise RuntimeError(json.dumps(msg["error"], ensure_ascii=False)[:800])
        res = msg.get("result", {})
        texts = [c.get("text", "") for c in res.get("content", []) if c.get("type") == "text"]
        out = "\n".join(texts)
        if res.get("isError"):
            raise RuntimeError(out[:2000])
        return out

    def tools(self):
        i = self._next()
        self._send({"jsonrpc": "2.0", "id": i, "method": "tools/list", "params": {}})
        return self._read(i, 120).get("result", {}).get("tools", [])

    def close(self):
        try:
            if self.proc:
                self.proc.kill()
        except Exception:
            pass


def extract_images(text):
    """Достаёт пути картинок из ответа MCP (look / generate_3d)."""
    import re
    return re.findall(r"[A-Za-z]:\\[^\s\"']+\.(?:png|jpg|jpeg)", text)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    mcp = BlenderMCP().start()
    try:
        if cmd == "list":
            for t in mcp.tools():
                print("-", t["name"], "|", (t.get("description") or "")[:100].replace("\n", " "))
                props = (t.get("inputSchema") or {}).get("properties", {})
                if props:
                    print("    args:", ", ".join(props.keys()))
        elif cmd == "code":
            code = sys.argv[2]
            print(mcp.call("execute_blender_code", {"code": code}))
        elif cmd == "look":
            mode = sys.argv[2] if len(sys.argv) > 2 else "scene"
            print(mcp.call("look", {"mode": mode}))
        elif cmd == "scene":
            print(mcp.call("get_scene_info", {}))
        elif cmd == "status":
            print(mcp.call("get_addon_status", {}))
        else:
            print("unknown command", cmd)
    finally:
        mcp.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
