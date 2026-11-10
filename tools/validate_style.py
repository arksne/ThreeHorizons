# -*- coding: utf-8 -*-
"""Ф3.7 · Gate A-1 — чек-лист худконтроля.

Проверяет ассет (запись манифеста `blender/manifest.json` или отдельный JSON) по 8 пунктам
из `GAME_DESIGN/Style.json → gateA1`. Каждый пункт даёт вердикт OK / FAIL с фактом.

Запуск:
    python -X utf8 tools/validate_style.py <манифест.json> [ассет.json ...]
    python -X utf8 tools/validate_style.py --manifest blender/manifest.json
Итог:  STYLE OK (exit 0)  или  STYLE FAIL + список (exit 1)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = ROOT / "GAME_DESIGN" / "Style.json"

STOCK_MATERIALS = set()
VALID_STATUS = {"concept", "blockout", "final", "lod"}
LOD1_TOL, LOD2_TOL = 0.03, 0.02
LOD1_TARGET, LOD2_TARGET = 0.35, 0.08


def load_style() -> dict:
    if not STYLE.exists():
        raise SystemExit("GAME_DESIGN/Style.json не найден — соберите: python -X utf8 tools/build_style.py")
    return json.loads(STYLE.read_text(encoding="utf-8"))


def known_hexes(style: dict) -> dict:
    out = {}
    for toks in style["factionTokens"].values():
        for t in toks:
            out[t["hex"].upper()] = t["id"]
    for t in style["uiTokens"]:
        out[t["hex"].upper()] = t["id"]
    for r in style["strategicResources"]:
        out[r["hex"].upper()] = r["id"]
    return out


def check_asset(a: dict, style: dict) -> list:
    """Возвращает список (id_пункта, ok, сообщение)."""
    res = []
    hexes = known_hexes(style)

    # 1. HEX из токенов
    used = [str(h).upper() for h in a.get("colors", a.get("hexes", []))]
    bad = [h for h in used if h not in hexes]
    if not used:
        res.append(("hexFromTokens", False, "не указаны цвета (colors/hexes)"))
    elif bad:
        res.append(("hexFromTokens", False,
                    f"цвета вне токенов: {', '.join(bad)}"))
    else:
        res.append(("hexFromTokens", True, f"{len(used)} цвет(ов) из токенов"))

    # 2. масштаб по MASTER_SCALE_SPEC
    dims = a.get("dimsM")
    want = a.get("expectedDimsM")
    if not dims:
        res.append(("scaleSpec", False, "не указан dimsM"))
    elif want and (abs(dims[0] - want[0]) > 0.01 or abs(dims[1] - want[1]) > 0.01):
        res.append(("scaleSpec", False, f"габарит {dims} ≠ заявленному {want}"))
    else:
        res.append(("scaleSpec", True, f"габарит {dims} м"))

    # 3. имя TH_*
    name = a.get("name", "")
    if not name.startswith("TH_"):
        res.append(("nameTH", False, f"имя «{name}» не начинается с TH_"))
    elif not name[3:].split("_")[0].isupper():
        res.append(("nameTH", False, f"префикс фракции в «{name}» не в верхнем регистре"))
    else:
        res.append(("nameTH", True, name))

    # 4. статус
    st = a.get("status", "")
    if st not in VALID_STATUS:
        res.append(("status", False, f"статус «{st}» не из {sorted(VALID_STATUS)}"))
    else:
        res.append(("status", True, st))

    # 5. материалов ≤ 3
    mats = a.get("materials", [])
    if len(mats) > 3:
        res.append(("materialsMax3", False, f"{len(mats)} материал(ов) > 3"))
    else:
        res.append(("materialsMax3", True, f"{len(mats)} материал(ов)"))

    # 6. UV
    uv = a.get("uvLayers", a.get("hasUV"))
    if uv is None:
        res.append(("hasUV", False, "не указано uvLayers/hasUV"))
    elif int(uv) <= 0:
        res.append(("hasUV", False, "UV-слой пуст"))
    else:
        res.append(("hasUV", True, f"UV-слоёв {uv}"))

    # 7. LOD 35 % / 8 %
    tri = a.get("tri", {})
    t0, t1, t2 = tri.get("L0"), tri.get("L1"), tri.get("L2")
    if not (t0 and t1 and t2):
        res.append(("lodRatio", False, "нет tri.L0/L1/L2"))
    else:
        r1, r2 = t1 / t0, t2 / t0
        if abs(r1 - LOD1_TARGET) > LOD1_TOL:
            res.append(("lodRatio", False, f"L1 = {r1 * 100:.1f} %, ждём {LOD1_TARGET * 100:.0f} % ±{LOD1_TOL * 100:.0f}"))
        elif abs(r2 - LOD2_TARGET) > LOD2_TOL:
            res.append(("lodRatio", False, f"L2 = {r2 * 100:.1f} %, ждём {LOD2_TARGET * 100:.0f} % ±{LOD2_TOL * 100:.0f}"))
        else:
            res.append(("lodRatio", True, f"L1 {r1 * 100:.0f} %, L2 {r2 * 100:.0f} %"))

    # 8. пивот в основании
    if a.get("origin") != "base_center":
        res.append(("pivotBase", False, f"origin = «{a.get('origin')}», ожидается base_center"))
    elif a.get("baseY", 0) != 0:
        res.append(("pivotBase", False, f"основание на y = {a.get('baseY')}, ожидается 0"))
    else:
        res.append(("pivotBase", True, "пивот в основании"))

    return res


def main() -> None:
    style = load_style()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit("укажите манифест: python -X utf8 tools/validate_style.py blender/manifest.json")

    assets = []
    for p in args:
        path = Path(p) if Path(p).is_absolute() else (ROOT / p)
        if not path.exists():
            raise SystemExit(f"файл не найден: {p}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            assets.extend(data)
        elif "assets" in data:
            assets.extend(data["assets"])
        else:
            assets.append(data)

    if not assets:
        raise SystemExit("в манифесте нет ассетов")

    total_ok = 0
    total = 0
    fails = []
    print("=== gate A-1: чек-лист худконтроля ===")
    for a in assets:
        name = a.get("name", "?")
        res = check_asset(a, style)
        bad = [r for r in res if not r[1]]
        total += len(res)
        total_ok += len(res) - len(bad)
        mark = "OK  " if not bad else "FAIL"
        print(f"  [{mark}] {name}")
        for pid, ok, msg in res:
            if not ok:
                print(f"         !! {pid}: {msg}")
        for pid, ok, msg in fails:
            pass
        fails.extend((name, pid, msg) for pid, ok, msg in res if not ok)

    print(f"\n  пунктов пройдено: {total_ok} из {total}")
    if fails:
        print(f"STYLE FAIL — нарушений: {len(fails)}")
        for name, pid, msg in fails:
            print(f"  !! {name}: {pid}: {msg}")
        raise SystemExit(1)
    print("STYLE OK")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
