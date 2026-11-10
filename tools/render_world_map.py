# -*- coding: utf-8 -*-
"""Ф2.5 · Генератор карты мира (PNG 2400×1600 + SVG).

Данные — из `GAME_DESIGN/World.json`. Рисует: 5 островов с подписями и высотой,
4 мини-острова, 4 маршрута (сплошные — грузовые, пунктир — пиратский рейд),
легенду, масштабную линейку и стрелку севера.

Раскладка: карта — в левой панели (по высоте), легенда и справка — в правой.

Запуск: python -X utf8 tools/render_world_map.py
Выход:  docs/world/WORLD_MAP.png
        docs/world/WORLD_MAP.svg
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
GD = ROOT / "GAME_DESIGN"
OUT = ROOT / "docs" / "world"

W, H = 2400, 1600

# --- панели ---
MAP_X, MAP_Y = 90, 150          # левый верх карты
MAP_MAX_W, MAP_MAX_H = 1150, 1330
PANEL_X = 1330                   # правая панель
PANEL_W = W - PANEL_X - 90

# палитра атласа (DESIGN_TOKENS: пергамент, латунь, чернила)
PAPER = (232, 220, 192)
PAPER_DARK = (203, 185, 143)
INK = (30, 26, 20)
BRASS = (176, 141, 62)
SEA_DEEP = (108, 130, 146)
GRID = (222, 210, 184)

FACTION_COLOR = {
    "arkvein": (58, 60, 66),       # ARK_GRAPHITE
    "valmer": (78, 126, 140),       # VAL_TEAL
    "grinwald": (90, 107, 60),      # GRN_OLIVE
    "esterholm": (138, 133, 120),   # GRN_STONE
    "black_harbor": (82, 43, 42),  # ARK_BURGUNDY
}
MINI_COLOR = (163, 132, 91)
ROUTE_COLOR = (58, 60, 66)
PIRATE_COLOR = (140, 43, 27)       # DANGER


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = (["arialbd.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"] if bold
             else ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"])
    for n in names:
        for base in (Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")):
            p = base / n
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), size)
                except OSError:
                    pass
    return ImageFont.load_default()


class Proj:
    """Игровые метры → пиксели."""

    def __init__(self, mw: float, md: float):
        self.s = min(MAP_MAX_W / mw, MAP_MAX_H / md)
        self.ox = MAP_X
        self.oy = MAP_Y
        self.mw, self.md = mw, md
        self.pw = mw * self.s
        self.ph = md * self.s

    def x(self, m: float) -> float:
        return self.ox + m * self.s

    def y(self, m: float) -> float:
        return self.oy + m * self.s


def load_world() -> dict:
    return json.loads((GD / "World.json").read_text(encoding="utf-8"))


def _dashed(d: ImageDraw.ImageDraw, p0, p1, col, width=4, dash=16, gap=11) -> None:
    x0, y0 = p0
    x1, y1 = p1
    total = math.hypot(x1 - x0, y1 - y0)
    if total == 0:
        return
    ux, uy = (x1 - x0) / total, (y1 - y0) / total
    t = 0.0
    while t < total:
        t2 = min(t + dash, total)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)], fill=col, width=width)
        t = t2 + gap


def _halo_text(d, xy, text, font, fill, anchor="mm", halo=PAPER, hw=4):
    """Текст с обводкой — читается и на тёмном острове, и на пергаменте."""
    d.text(xy, text, font=font, fill=fill, anchor=anchor,
           stroke_width=hw, stroke_fill=halo)


def draw_map(world: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_title = font(52, bold=True)
    f_sub = font(24)
    f_panel_h = font(30, bold=True)
    f_city = font(25, bold=True)
    f_h = font(20, bold=True)
    f_small = font(20)
    f_tiny = font(17)
    f_leg = font(22)

    mw, md = world["frame"]["mapGameM"]
    p = Proj(mw, md)

    # ---------- шапка ----------
    d.text((MAP_X, 44), "ТРИ ГОРИЗОНТА — КАРТА МИРА", font=f_title, fill=INK)
    d.text((MAP_X, 104), "Рамка S-07: атлас + 18×26 км игровых · 1 лор-км = 100 м · "
                         "высоты — над облачным морем (Y=0)", font=f_sub, fill=INK)

    # ---------- море и сетка ----------
    for gx in range(0, int(mw) + 1, 2000):
        d.line([(p.x(gx), p.y(0)), (p.x(gx), p.y(md))], fill=GRID, width=1)
    for gz in range(0, int(md) + 1, 2000):
        d.line([(p.x(0), p.y(gz)), (p.x(mw), p.y(gz))], fill=GRID, width=1)
    d.rectangle([p.x(0), p.y(0), p.x(mw), p.y(md)], outline=SEA_DEEP, width=4)

    by_id = {i["id"]: i for i in world["islands"]}

    # ---------- маршруты (под островами) ----------
    for rid, t in world["travelTimes"].items():
        a, b = by_id.get(t["from"]), by_id.get(t["to"])
        if not a or not b:
            continue
        pirate = t["type"] == "contraband" or rid == "pirate_raid"
        col = PIRATE_COLOR if pirate else ROUTE_COLOR
        p0 = (p.x(a["gameXM"]), p.y(a["gameZM"]))
        p1 = (p.x(b["gameXM"]), p.y(b["gameZM"]))
        if pirate:
            _dashed(d, p0, p1, col, width=5, dash=20, gap=13)
        else:
            d.line([p0, p1], fill=col, width=5)

    # ---------- мини-острова ----------
    for m in world["miniIslands"]:
        cx, cz = p.x(m["gameXM"]), p.y(m["gameZM"])
        r = max(8, min(p.s * m["gameWM"], p.s * m["gameDM"]) / 2)
        d.polygon([(cx, cz - r), (cx + r, cz), (cx, cz + r), (cx - r, cz)],
                  fill=MINI_COLOR, outline=INK)
        _halo_text(d, (cx + r + 12, cz), m["id"], f_tiny, INK, anchor="lm")

    # ---------- острова ----------
    for i in world["islands"]:
        x0, x1 = p.x(i["gameXM"] - i["gameWM"] / 2), p.x(i["gameXM"] + i["gameWM"] / 2)
        z0, z1 = p.y(i["gameZM"] - i["gameDM"] / 2), p.y(i["gameZM"] + i["gameDM"] / 2)
        col = FACTION_COLOR.get(i["faction"], MINI_COLOR)
        d.rounded_rectangle([x0, z0, x1, z1], radius=9, fill=col, outline=INK, width=3)
        cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
        wide = (x1 - x0) > 150
        if wide:
            # подпись внутри
            _halo_text(d, (cx, cz - 12), i["name"], f_city, PAPER, halo=INK, hw=3)
            _halo_text(d, (cx, cz + 16), f"{i['heightM']} м", f_tiny, PAPER_DARK, halo=INK, hw=3)
        else:
            # подпись рядом, с выноской
            lx = x1 + 14
            d.line([(x1, cz), (lx - 4, cz)], fill=INK, width=2)
            _halo_text(d, (lx, cz - 10), i["name"], f_h, INK, anchor="lm")
            _halo_text(d, (lx, cz + 12), f"{i['heightM']} м", f_tiny, INK, anchor="lm")

    # ---------- стрелка севера ----------
    nx, ny = MAP_X + p.pw - 40, MAP_Y - 46
    d.polygon([(nx, ny), (nx - 15, ny + 34), (nx + 15, ny + 34)], fill=INK)
    d.text((nx, ny + 38), "N", font=f_h, fill=INK, anchor="ma")

    # ---------- масштабная линейка (под картой) ----------
    km = 2
    px = km * 1000 * p.s
    bx, by = MAP_X, MAP_Y + p.ph + 34
    d.rectangle([bx, by, bx + px, by + 13], fill=INK)
    d.text((bx, by + 20), f"{km} км", font=f_small, fill=INK)
    d.text((bx + px + 28, by), f"карта {mw/1000:.0f}×{md/1000:.0f} км игровых = "
                               f"{world['frame']['mapStuds'][0]}×{world['frame']['mapStuds'][1]} st",
           font=f_small, fill=INK)

    # ---------- правая панель ----------
    px0 = PANEL_X
    d.line([(px0 - 40, MAP_Y - 40), (px0 - 40, H - 60)], fill=BRASS, width=3)

    d.text((px0, MAP_Y - 30), "ЛЕГЕНДА", font=f_panel_h, fill=INK)
    ly = MAP_Y + 20
    legend = [
        ("island", "Остров (высота — над морем)"),
        ("mini", "Мини-остров (промысловый)"),
        ("route", "Грузовой маршрут"),
        ("pirate", "Пиратский рейд"),
    ]
    for kind, text in legend:
        if kind == "island":
            d.rectangle([px0, ly, px0 + 26, ly + 18], fill=SEA_DEEP, outline=INK, width=2)
        elif kind == "mini":
            d.polygon([(px0 + 13, ly), (px0 + 26, ly + 9), (px0 + 13, ly + 18), (px0, ly + 9)],
                      fill=MINI_COLOR, outline=INK)
        elif kind == "route":
            d.line([(px0, ly + 9), (px0 + 26, ly + 9)], fill=ROUTE_COLOR, width=5)
        else:
            _dashed(d, (px0, ly + 9), (px0 + 26, ly + 9), PIRATE_COLOR, width=5, dash=10, gap=7)
        d.text((px0 + 42, ly - 2), text, font=f_leg, fill=INK)
        ly += 32

    # острова списком с высотой
    ly += 16
    d.text((px0, ly), "ОСТРОВА", font=f_panel_h, fill=INK)
    ly += 40
    for i in world["islands"]:
        col = FACTION_COLOR.get(i["faction"], MINI_COLOR)
        d.rectangle([px0, ly + 3, px0 + 22, ly + 19], fill=col, outline=INK, width=2)
        d.text((px0 + 36, ly), f"{i['name']} — {i['heightM']} м", font=f_leg, fill=INK)
        ly += 30

    # мини-острова
    ly += 12
    d.text((px0, ly), "МИНИ-ОСТРОВА (S-10)", font=f_panel_h, fill=INK)
    ly += 40
    for m in world["miniIslands"]:
        d.polygon([(px0 + 11, ly), (px0 + 22, ly + 8), (px0 + 11, ly + 16), (px0, ly + 8)],
                  fill=MINI_COLOR, outline=INK)
        d.text((px0 + 36, ly), f"{m['id']} · {m['name']}", font=f_small, fill=INK)
        ly += 26

    # маршруты с временем
    ly += 12
    d.text((px0, ly), "МАРШРУТЫ (18 м/с)", font=f_panel_h, fill=INK)
    ly += 40
    for rid, t in world["travelTimes"].items():
        pirate = t["type"] == "contraband" or rid == "pirate_raid"
        col = PIRATE_COLOR if pirate else ROUTE_COLOR
        d.line([(px0, ly + 8), (px0 + 22, ly + 8)], fill=col, width=4)
        names = {i["id"]: i["name"] for i in world["islands"]}
        d.text((px0 + 36, ly), f"{names.get(t['from'], t['from'])} → "
                               f"{names.get(t['to'], t['to'])}", font=f_small, fill=INK)
        d.text((px0 + 36, ly + 21), f"{t['distanceGameM']:.0f} м · {t['minutes']:.1f} мин",
               font=f_tiny, fill=INK)
        ly += 48

    # ---------- подвал правой панели ----------
    fy = H - 190
    d.text((px0, fy), "ИСТОЧНИК", font=f_panel_h, fill=INK)
    fy += 38
    for line in ("GAME_DESIGN/World.json — истина по геометрии",
                 "docs/world/WORLD_COORDINATES.csv — экспорт",
                 "tools/build_world.py — пересчёт из constants.json",
                 "Правило канона: текст важнее арта (D-001)",
                 "Рамка и позиции — DECISIONS.md S-07…S-11"):
        d.text((px0, fy), line, font=f_small, fill=INK)
        fy += 27
    return img


def write_svg(world: dict) -> Path:
    """SVG-версия: карта в левой панели, легенда — справа."""
    mw, md = world["frame"]["mapGameM"]
    p = Proj(mw, md)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#E8DCC0"/>',
         f'<text x="{MAP_X}" y="78" font-family="Georgia,serif" font-size="50" '
         f'font-weight="bold" fill="#1E1A14">ТРИ ГОРИЗОНТА — КАРТА МИРА</text>',
         f'<text x="{MAP_X}" y="116" font-family="sans-serif" font-size="22" fill="#1E1A14">'
         f'Рамка S-07: атлас + 18×26 км игровых · 1 лор-км = 100 м · '
         f'высоты — над облачным морем (Y=0)</text>',
         f'<rect x="{p.x(0):.1f}" y="{p.y(0):.1f}" width="{p.pw:.1f}" height="{p.ph:.1f}" '
         f'fill="none" stroke="#6C8292" stroke-width="4"/>']

    by_id = {i["id"]: i for i in world["islands"]}
    for rid, t in world["travelTimes"].items():
        a, b = by_id.get(t["from"]), by_id.get(t["to"])
        if not a or not b:
            continue
        pirate = t["type"] == "contraband" or rid == "pirate_raid"
        col = "#8C2B1B" if pirate else "#3A3C42"
        dash = ' stroke-dasharray="20,13"' if pirate else ""
        o.append(f'<line x1="{p.x(a["gameXM"]):.1f}" y1="{p.y(a["gameZM"]):.1f}" '
                 f'x2="{p.x(b["gameXM"]):.1f}" y2="{p.y(b["gameZM"]):.1f}" '
                 f'stroke="{col}" stroke-width="5"{dash}/>')

    for m in world["miniIslands"]:
        cx, cy = p.x(m["gameXM"]), p.y(m["gameZM"])
        r = max(8, min(p.s * m["gameWM"], p.s * m["gameDM"]) / 2)
        o.append(f'<polygon points="{cx:.1f},{cy-r:.1f} {cx+r:.1f},{cy:.1f} '
                 f'{cx:.1f},{cy+r:.1f} {cx-r:.1f},{cy:.1f}" fill="#A3845B" stroke="#1E1A14"/>')
        o.append(f'<text x="{cx+r+12:.1f}" y="{cy+6:.1f}" font-family="sans-serif" '
                 f'font-size="17" fill="#1E1A14">{m["id"]}</text>')

    COL = {"arkvein": "#3A3C42", "valmer": "#4E7E8C", "grinwald": "#5A6B3C",
           "esterholm": "#8A8578", "black_harbor": "#522B2A"}
    for i in world["islands"]:
        x0 = p.x(i["gameXM"] - i["gameWM"] / 2)
        y0 = p.y(i["gameZM"] - i["gameDM"] / 2)
        w, h = i["gameWM"] * p.s, i["gameDM"] * p.s
        cx, cy = x0 + w / 2, y0 + h / 2
        o.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'rx="9" fill="{COL.get(i["faction"], "#A3845B")}" stroke="#1E1A14" '
                 f'stroke-width="3"/>')
        if w > 150:
            o.append(f'<text x="{cx:.1f}" y="{cy-2:.1f}" font-family="Georgia,serif" '
                     f'font-size="25" font-weight="bold" fill="#E8DCC0" '
                     f'text-anchor="middle">{i["name"]}</text>')
            o.append(f'<text x="{cx:.1f}" y="{cy+24:.1f}" font-family="sans-serif" '
                     f'font-size="17" fill="#CBB98F" text-anchor="middle">'
                     f'{i["heightM"]} м</text>')
        else:
            o.append(f'<line x1="{x0+w:.1f}" y1="{cy:.1f}" x2="{x0+w+12:.1f}" '
                     f'y2="{cy:.1f}" stroke="#1E1A14" stroke-width="2"/>')
            o.append(f'<text x="{x0+w+16:.1f}" y="{cy-2:.1f}" font-family="sans-serif" '
                     f'font-size="20" font-weight="bold" fill="#1E1A14">'
                     f'{i["name"]}</text>')
            o.append(f'<text x="{x0+w+16:.1f}" y="{cy+20:.1f}" font-family="sans-serif" '
                     f'font-size="17" fill="#1E1A14">{i["heightM"]} м</text>')

    px = 2 * 1000 * p.s
    bx, by = MAP_X, MAP_Y + p.ph + 34
    o.append(f'<rect x="{bx}" y="{by}" width="{px:.1f}" height="13" fill="#1E1A14"/>')
    o.append(f'<text x="{bx}" y="{by+40}" font-family="sans-serif" font-size="20" '
             f'fill="#1E1A14">2 км</text>')

    # правая панель
    o.append(f'<line x1="{PANEL_X-40}" y1="{MAP_Y-40}" x2="{PANEL_X-40}" y2="{H-60}" '
             f'stroke="#B08D3E" stroke-width="3"/>')
    o.append(f'<text x="{PANEL_X}" y="{MAP_Y-16}" font-family="Georgia,serif" font-size="30" '
             f'font-weight="bold" fill="#1E1A14">ЛЕГЕНДА</text>')
    ly = MAP_Y + 24
    for kind, text, col, poly in (
            ("island", "Остров (высота — над морем)", "#6C8292", False),
            ("mini", "Мини-остров (промысловый)", "#A3845B", True),
            ("route", "Грузовой маршрут", "#3A3C42", False),
            ("pirate", "Пиратский рейд", "#8C2B1B", False)):
        if poly:
            o.append(f'<polygon points="{PANEL_X+11},{ly} {PANEL_X+22},{ly+8} '
                     f'{PANEL_X+11},{ly+16} {PANEL_X},{ly+8}" fill="{col}" stroke="#1E1A14"/>')
        else:
            dash = ' stroke-dasharray="10,7"' if kind == "pirate" else ""
            o.append(f'<line x1="{PANEL_X}" y1="{ly+8}" x2="{PANEL_X+22}" y2="{ly+8}" '
                     f'stroke="{col}" stroke-width="5"{dash}/>')
        o.append(f'<text x="{PANEL_X+42}" y="{ly+16}" font-family="sans-serif" '
                 f'font-size="22" fill="#1E1A14">{text}</text>')
        ly += 32

    ly += 16
    o.append(f'<text x="{PANEL_X}" y="{ly+20}" font-family="Georgia,serif" font-size="30" '
             f'font-weight="bold" fill="#1E1A14">ОСТРОВА</text>')
    ly += 52
    for i in world["islands"]:
        o.append(f'<rect x="{PANEL_X}" y="{ly}" width="22" height="17" '
                 f'fill="{COL.get(i["faction"], "#A3845B")}" stroke="#1E1A14" stroke-width="2"/>')
        o.append(f'<text x="{PANEL_X+36}" y="{ly+16}" font-family="sans-serif" font-size="22" '
                 f'fill="#1E1A14">{i["name"]} — {i["heightM"]} м</text>')
        ly += 30

    ly += 12
    o.append(f'<text x="{PANEL_X}" y="{ly+20}" font-family="Georgia,serif" font-size="30" '
             f'font-weight="bold" fill="#1E1A14">МАРШРУТЫ (18 м/с)</text>')
    ly += 52
    names = {i["id"]: i["name"] for i in world["islands"]}
    for rid, t in world["travelTimes"].items():
        pirate = t["type"] == "contraband" or rid == "pirate_raid"
        col = "#8C2B1B" if pirate else "#3A3C42"
        dash = ' stroke-dasharray="14,9"' if pirate else ""
        o.append(f'<line x1="{PANEL_X}" y1="{ly+8}" x2="{PANEL_X+22}" y2="{ly+8}" '
                 f'stroke="{col}" stroke-width="4"{dash}/>')
        o.append(f'<text x="{PANEL_X+36}" y="{ly+16}" font-family="sans-serif" font-size="20" '
                 f'fill="#1E1A14">{names.get(t["from"], t["from"])} → '
                 f'{names.get(t["to"], t["to"])}</text>')
        o.append(f'<text x="{PANEL_X+36}" y="{ly+40}" font-family="sans-serif" font-size="17" '
                 f'fill="#1E1A14">{t["distanceGameM"]:.0f} м · {t["minutes"]:.1f} мин</text>')
        ly += 52

    fy = H - 190
    o.append(f'<text x="{PANEL_X}" y="{fy+20}" font-family="Georgia,serif" font-size="30" '
             f'font-weight="bold" fill="#1E1A14">ИСТОЧНИК</text>')
    for k, line in enumerate((
            "GAME_DESIGN/World.json — истина по геометрии",
            "docs/world/WORLD_COORDINATES.csv — экспорт",
            "tools/build_world.py — пересчёт из constants.json",
            "Правило канона: текст важнее арта (D-001)",
            "Рамка и позиции — DECISIONS.md S-07…S-11")):
        o.append(f'<text x="{PANEL_X}" y="{fy+58+k*27}" font-family="sans-serif" '
                 f'font-size="20" fill="#1E1A14">{line}</text>')
    o.append("</svg>")
    pth = OUT / "WORLD_MAP.svg"
    pth.write_text("\n".join(o), encoding="utf-8")
    return pth


def main() -> None:
    world = load_world()
    OUT.mkdir(parents=True, exist_ok=True)
    img = draw_map(world)
    png = OUT / "WORLD_MAP.png"
    img.save(png, "PNG")
    svg = write_svg(world)
    print(f"OK {png.name}: {img.size[0]}×{img.size[1]}, {png.stat().st_size // 1024} KB")
    print(f"OK {svg.name}: {svg.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
