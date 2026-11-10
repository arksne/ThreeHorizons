# -*- coding: utf-8 -*-
"""PNG-превью любого .canvas: python preview_roadmap.py <in.canvas> <out.png> [scale]"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FILL = {
    "1": (251, 70, 76), "2": (233, 151, 63), "3": (224, 222, 113),
    "4": (68, 207, 110), "5": (83, 223, 221), "6": (168, 130, 255),
}
FD = Path("C:/Windows/Fonts")


def wrap(draw, text, font, width):
    out = []
    for para in text.replace("**", "").replace("`", "").split("\n"):
        if not para.strip():
            out.append("")
            continue
        cur = ""
        for word in para.split(" "):
            probe = (cur + " " + word).strip()
            if draw.textlength(probe, font=font) <= width or not cur:
                cur = probe
            else:
                out.append(cur)
                cur = word
        out.append(cur)
    return out


def validate(nodes):
    bad = []
    for g in [n for n in nodes if n["type"] == "group"]:
        gx1, gy1 = g["x"] + g["width"], g["y"] + g["height"]
        for c in [n for n in nodes if n["type"] == "text"]:
            cx, cy = c["x"] + c["width"] / 2, c["y"] + c["height"] / 2
            if not (g["x"] <= cx <= gx1 and g["y"] <= cy <= gy1):
                continue
            if c["x"] < g["x"] - 2 or c["y"] < g["y"] - 2 or \
               c["x"] + c["width"] > gx1 + 2 or c["y"] + c["height"] > gy1 + 2:
                bad.append(f"{c['id']} вне {g['id']}")
    return bad


def main():
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    pad = 60
    data = json.loads(src.read_text(encoding="utf-8"))
    nodes = data["nodes"]
    for p in validate(nodes):
        print("WARN:", p)
    print("nodes:", len(nodes), "| edges:", len(data.get("edges", [])),
          "| ids unique:", len({n["id"] for n in nodes}) == len(nodes))

    f_txt = ImageFont.truetype(str(FD / "segoeui.ttf"), max(8, int(12 * scale)))
    f_grp = ImageFont.truetype(str(FD / "segoeuib.ttf"), max(9, int(14 * scale)))

    minx = min(n["x"] for n in nodes) - pad
    miny = min(n["y"] for n in nodes) - pad
    maxx = max(n["x"] + n["width"] for n in nodes) + pad
    maxy = max(n["y"] + n["height"] for n in nodes) + pad
    W, H = int((maxx - minx) * scale), int((maxy - miny) * scale)
    img = Image.new("RGB", (W, H), (30, 31, 34))
    d = ImageDraw.Draw(img, "RGBA")
    sx = lambda v: (v - minx) * scale
    sy = lambda v: (v - miny) * scale

    for n in nodes:
        if n["type"] != "group":
            continue
        box = [sx(n["x"]), sy(n["y"]), sx(n["x"] + n["width"]), sy(n["y"] + n["height"])]
        d.rounded_rectangle(box, 6, fill=(255, 255, 255, 8), outline=(255, 255, 255, 40), width=1)
        d.text((box[0] + 6, box[1] + 5), n.get("label", ""), font=f_grp, fill=(205, 205, 210))

    by_id = {n["id"]: n for n in nodes}
    for e in data.get("edges", []):
        a, b = by_id.get(e["fromNode"]), by_id.get(e["toNode"])
        if not a or not b:
            continue
        x1, y1 = sx(a["x"] + a["width"]), sy(a["y"] + min(a["height"] * 0.2, 120))
        x2, y2 = sx(b["x"]), sy(b["y"] + min(b["height"] * 0.2, 120))
        mid = (x1 + x2) / 2
        col = FILL.get(e.get("color", ""), (140, 140, 150))
        d.line([(x1, y1), (mid, y1), (mid, y2), (x2, y2)], fill=col + (170,), width=1)
        d.polygon([(x2, y2), (x2 - 5, y2 - 3), (x2 - 5, y2 + 3)], fill=col + (200,))

    for n in nodes:
        if n["type"] != "text":
            continue
        x0, y0 = sx(n["x"]), sy(n["y"])
        x1, y1 = sx(n["x"] + n["width"]), sy(n["y"] + n["height"])
        color = FILL.get(n.get("color", ""), (110, 110, 120))
        d.rounded_rectangle([x0, y0, x1, y1], 4, fill=color + (44,), outline=color + (190,), width=1)
        ty = y0 + 4
        for line in wrap(d, n["text"], f_txt, (x1 - x0) - 10):
            if ty > y1 - 4:
                break
            d.text((x0 + 5, ty), line, font=f_txt, fill=(233, 233, 238))
            ty += 12 * scale + 2

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"OK {out} | {W}x{H}")


if __name__ == "__main__":
    main()
