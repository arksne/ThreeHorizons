import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

API = "https://api.github.com"


def cred():
    out = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True).stdout
    d = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            d[k] = v
    return d


def api(method, path, body=None, token=None, accept="application/vnd.github+json"):
    c = cred()
    hdr = {
        "Authorization": f"token {token or c['password']}",
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "three-horizons-tool",
    }
    data = json.dumps(body).encode() if body is not None else None
    if data:
        hdr["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, headers=hdr, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw[:400]}


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else "arksne/ThreeHorizons"
    action = sys.argv[2] if len(sys.argv) > 2 else "status"
    st, info = api("GET", f"/repos/{repo}")
    print("repo:", repo, "| status", st)
    if st == 200:
        print("  visibility:", info.get("visibility"), "| private:", info.get("private"),
              "| owner:", info.get("owner", {}).get("login"),
              "| default_branch:", info.get("default_branch"),
              "| size_kb:", info.get("size"))
        print("  collaborators_perm:", info.get("permissions"))
    if action == "public":
        st, res = api("PATCH", f"/repos/{repo}", {"visibility": "public", "private": False})
        print("PATCH ->", st, res.get("visibility") if isinstance(res, dict) else res)
        if st == 200:
            st2, info2 = api("GET", f"/repos/{repo}")
            print("  now:", info2.get("visibility"), "| html:", info2.get("html_url"))
    elif action == "collaborator":
        user = sys.argv[3]
        perm = sys.argv[4] if len(sys.argv) > 4 else "push"
        st, res = api("PUT", f"/repos/{repo}/collaborators/{user}", {"permission": perm})
        print("add collaborator ->", st, res.get("message") if isinstance(res, dict) else res)
    elif action == "list":
        st, res = api("GET", f"/repos/{repo}/collaborators")
        if isinstance(res, list):
            for c in res:
                print("  ", c.get("login"), c.get("role_name") or c.get("permissions"))
        else:
            print(st, res)


if __name__ == "__main__":
    main()
