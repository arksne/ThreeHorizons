"""Higgsfield MCP OAuth (PKCE) helper for the Three Horizons ref-generation pipeline.

Registers a local OAuth client, opens the browser authorize URL, captures the
redirect on 127.0.0.1:8765 and stores the token bundle outside the repo.
"""
import base64, hashlib, json, os, secrets, sys, threading, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.stdout.reconfigure(encoding="utf-8")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
AS = "https://clerk.higgsfield.ai"
REDIRECT = "http://127.0.0.1:8765/callback"
SCOPE = "openid email offline_access"
RESOURCE = "https://mcp.higgsfield.ai/mcp"
TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".higgsfield-mcp-token.json")


def http_json(method, url, data=None, headers=None, timeout=30):
    h = {"Accept": "application/json", "User-Agent": UA}
    if headers:
        h.update(headers)
    body = None
    if data is not None:
        if headers and "form" in headers.get("Content-Type", ""):
            body = urllib.parse.urlencode(data).encode()
        else:
            body = json.dumps(data).encode()
            h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def register_client():
    st, body = http_json("POST", AS + "/oauth/register", {
        "client_name": "three-horizons-refgen",
        "application_type": "native",
        "redirect_uris": [REDIRECT],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    })
    if st not in (200, 201):
        raise SystemExit(f"register failed: {st} {body[:400]}")
    return json.loads(body)["client_id"]


def pkce():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).decode().rstrip("=")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return verifier, challenge


def wait_for_code(state):
    holder = {}

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            holder["code"] = (q.get("code") or [None])[0]
            holder["state"] = (q.get("state") or [None])[0]
            holder["error"] = (q.get("error") or [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body style='font-family:sans-serif;padding:40px'>"
                             b"<h2>Higgsfield authorized.</h2>"
                             b"<p>You can close this tab and return to OpenCode.</p></body></html>")
            threading.Thread(target=server.shutdown, daemon=True).start()

        def log_message(self, *a):
            pass

    server = HTTPServer(("127.0.0.1", 8765), H)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    for _ in range(600):
        if holder.get("code") or holder.get("error"):
            break
        import time
        time.sleep(1)
    server.shutdown()
    return holder


def main():
    client_id = register_client()
    verifier, challenge = pkce()
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT,
        "scope": SCOPE,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "resource": RESOURCE,
    }
    url = AS + "/oauth/authorize?" + urllib.parse.urlencode(params)
    print("CLIENT_ID=" + client_id, flush=True)
    print("AUTHORIZE_URL=" + url, flush=True)
    print("Waiting for the browser redirect on " + REDIRECT + " ...", flush=True)
    print("WAITING_FOR_BROWSER=1", flush=True)
    res = wait_for_code(state)
    print("CALLBACK=" + json.dumps(res)[:300], flush=True)
    if not res.get("code"):
        print("FAILED: " + str(res.get("error")), flush=True)
        return 1
    st, body = http_json("POST", AS + "/oauth/token", {
        "grant_type": "authorization_code",
        "code": res["code"],
        "redirect_uri": REDIRECT,
        "client_id": client_id,
        "code_verifier": verifier,
        "resource": RESOURCE,
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    print("TOKEN_STATUS=" + str(st), flush=True)
    if st not in (200, 201):
        print(body[:600], flush=True)
        return 2
    tok = json.loads(body)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(tok, f, indent=1)
    print("TOKEN_SAVED=" + TOKEN_FILE, flush=True)
    print("SCOPES=" + str(tok.get("scope")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
