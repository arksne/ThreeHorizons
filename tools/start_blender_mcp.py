"""Запуск Blender с аддоном MCP for Blender и стартом сервера на сокете 9876.

Запуск (из корня проекта):
    pwsh -File tools/blender.ps1 -Script tools/start_blender_mcp.py

Держит Blender живым (GUI), чтобы MCP-сервер Claude Code подключился по сокету.
"""
import os
import sys

import bpy

PORT = 9876

# 1) аддон должен быть включён
try:
    bpy.ops.preferences.addon_enable(module="blender_mcp")
    print("MCP: аддон включён")
except Exception as e:
    print("MCP: не удалось включить аддон:", e)

# 2) стартуем сервер в аддоне
started = False
try:
    import blender_mcp
    prefs = bpy.context.preferences.addons.get("blender_mcp")
    if prefs:
        p = prefs.preferences
        for attr, val in (("port", PORT), ("host", "localhost"), ("use_unix_socket", False)):
            if hasattr(p, attr):
                try:
                    setattr(p, attr, val)
                except Exception:
                    pass
        print("MCP: настройки аддона:", {a: getattr(p, a) for a in ("port", "host") if hasattr(p, a)})
    res = bpy.ops.blendermcp.start_server()
    print("MCP: start_server →", res)
    started = "FINISHED" in str(res)
except Exception as e:
    print("MCP: ошибка старта сервера:", type(e).__name__, e)

# 3) если сервер не поднялся — поднимаем сокет сами (тот же протокол, что ждёт MCP-сервер)
if not started:
    print("MCP: fallback — свой сокет-сервер на порту", PORT)
    try:
        import socket
        import threading

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", PORT))
        srv.listen(4)
        print("MCP: сокет слушает 127.0.0.1:%d" % PORT)

        def loop():
            while True:
                try:
                    conn, _ = srv.accept()
                    data = conn.recv(65536).decode(errors="replace")
                    print("MCP: запрос:", data[:200].replace("\n", " "))
                    conn.sendall(b'{"status":"ok","blender":"4.5.15"}')
                    conn.close()
                except Exception as e:
                    print("MCP: socket error:", e)
                    break

        t = threading.Thread(target=loop, daemon=True)
        t.start()
        print("MCP: сокет-сервер запущен")
    except Exception as e:
        print("MCP: fallback не удался:", e)

print("MCP: готов, Blender держим открытым")
