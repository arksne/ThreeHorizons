# -*- coding: utf-8 -*-
"""Поднимает версию проекта в одном месте (version.json) и печатает блок для CHANGELOG.

Использование:
  python -X utf8 tools/bump_version.py patch   # 0.1.0 -> 0.1.1
  python -X utf8 tools/bump_version.py minor   # 0.1.0 -> 0.2.0
  python -X utf8 tools/bump_version.py major   # 0.1.0 -> 1.0.0
  python -X utf8 tools/bump_version.py show    # только показать
"""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VER = ROOT / "version.json"


def main() -> None:
    data = json.loads(VER.read_text(encoding="utf-8"))
    cur = data.get("version", "0.0.0")
    part = (sys.argv[1] if len(sys.argv) > 1 else "show").lower()

    major, minor, patch = (int(x) for x in cur.split("."))
    if part == "patch":
        patch += 1
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part != "show":
        raise SystemExit("аргумент: patch | minor | major | show")

    new = f"{major}.{minor}.{patch}"
    if part != "show":
        data["version"] = new
        data["updated"] = datetime.date.today().isoformat()
        VER.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"version: {cur} -> {new}")
    print("\nблок для docs/CHANGELOG.md:\n")
    print(f"## v{new} — {datetime.date.today().isoformat()}\n")
    print("- <что сделано>\n")


if __name__ == "__main__":
    main()
