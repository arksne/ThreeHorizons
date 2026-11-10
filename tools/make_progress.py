# -*- coding: utf-8 -*-
"""
Прогресс роадмапа: docs/PROGRESS.json — единственный источник статусов шагов.

Статусы: todo | in_progress | done | blocked | skipped
Канвасы окрашиваются по этому файлу (генератор make_roadmap_canvas.py).

Запуск:
  python -X utf8 tools/make_progress.py            # создать/дополнить, сохранив текущие статусы
  python -X utf8 tools/make_progress.py 0.1 done   # выставить статус шагу
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASES_DIR = ROOT / "docs" / "roadmap"
OUT = ROOT / "docs" / "PROGRESS.json"
VALID = {"todo", "in_progress", "done", "blocked", "skipped"}


def scan_steps() -> list[str]:
    nums = []
    for path in sorted(PHASES_DIR.glob("phase-*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"###\s+(\S+)\s*·\s*(.+)", line)
            if m:
                nums.append(m.group(1))
    return nums


def main() -> None:
    steps = scan_steps()
    data = {"version": "0.1", "updated": "", "steps": {n: "todo" for n in steps}}
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        for num in steps:
            data["steps"][num] = old.get("steps", {}).get(num, "todo")

    if len(sys.argv) >= 3:
        num, status = sys.argv[1], sys.argv[2]
        if num not in data["steps"]:
            raise SystemExit(f"нет шага {num}")
        if status not in VALID:
            raise SystemExit(f"неизвестный статус {status}; допустимо: {sorted(VALID)}")
        data["steps"][num] = status

    import datetime
    data["updated"] = datetime.date.today().isoformat()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    counts = {}
    for st in data["steps"].values():
        counts[st] = counts.get(st, 0) + 1
    print(f"OK {OUT} | steps={len(steps)} | " +
          " ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
