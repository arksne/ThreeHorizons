"""Подготовка референса к image-to-3D.

Референсы — технические листы: объект на плохом сером фоне #B8BEB4 плюс
линейка и силуэт человека. Для 3D нужен только объект, без вспомогательных
силуэтов, поэтому:

1. маска «не фон» (по цвету фона),
2. связные компоненты, берём самую большую (сам объект),
3. кроп по её bbox, выравнивание по центру, квадрат 1024x1024, белый фон.

    python prep_object.py --in refs/trawler.png --out model_src/trawler.png
"""
import argparse
import os
import sys
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image
import numpy as np

BG = (184, 190, 180)  # #B8BEB4
TOL = 16
MASK_SIZE = 512


def largest_component_bbox(rgb):
    """bbox самой большой связной области «не фон» (считаем на уменьшенной копии)."""
    h, w = rgb.shape[:2]
    step = max(1, max(h, w) // MASK_SIZE)
    small = rgb[::step, ::step]
    bg = np.array(BG, dtype=np.int16)
    dist = np.abs(small.astype(np.int16) - bg).sum(axis=2)
    mask = dist > TOL * 3
    h2, w2 = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    best = None
    best_size = 0
    for sy in range(h2):
        for sx in range(w2):
            if not mask[sy, sx] or seen[sy, sx]:
                continue
            q = deque([(sy, sx)])
            seen[sy, sx] = True
            size = 0
            miny = maxy = sy
            minx = maxx = sx
            while q:
                y, x = q.popleft()
                size += 1
                if y < miny: miny = y
                if y > maxy: maxy = y
                if x < minx: minx = x
                if x > maxx: maxx = x
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h2 and 0 <= nx < w2 and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if size > best_size:
                best_size = size
                best = (miny, minx, maxy, maxx)
    if best is None:
        return (0, 0, w, h)
    miny, minx, maxy, maxx = best
    return (minx * step, miny * step, (maxx + 1) * step, (maxy + 1) * step)


def prepare(src, dst, size=1024, pad=0.06):
    im = Image.open(src).convert("RGB")
    rgb = np.asarray(im)
    x0, y0, x1, y1 = largest_component_bbox(rgb)
    bw, bh = x1 - x0, y1 - y0
    m = int(max(bw, bh) * pad)
    x0 = max(0, x0 - m); y0 = max(0, y0 - m)
    x1 = min(im.width, x1 + m); y1 = min(im.height, y1 + m)
    crop = im.crop((x0, y0, x1, y1))

    # нейтральный фон: чистый белый — так image-to-3D меньше путает с цветом
    canvas = Image.new("RGB", (size, size), (255, 255, 255))
    scale = (size * 0.92) / max(crop.width, crop.height)
    new = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.LANCZOS)
    canvas.paste(new, ((size - new.width) // 2, (size - new.height) // 2))
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    canvas.save(dst)
    return {"source": src, "out": dst, "bbox": [x0, y0, x1, y1], "size": size}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    ap.add_argument("--size", type=int, default=1024)
    ap.add_argument("--keep-bg", action="store_true", help="не вырезать фон, просто ресайз")
    args = ap.parse_args()
    if args.keep_bg:
        im = Image.open(args.src).convert("RGB").resize((args.size, args.size), Image.LANCZOS)
        os.makedirs(os.path.dirname(os.path.abspath(args.dst)), exist_ok=True)
        im.save(args.dst)
        print(f"{args.src} -> {args.dst} (resize only)")
        return
    info = prepare(args.src, args.dst, args.size)
    print(f"{args.src} -> {args.dst} bbox={info['bbox']}")


if __name__ == "__main__":
    main()
