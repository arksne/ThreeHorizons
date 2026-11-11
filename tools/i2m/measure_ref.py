"""Измерение силуэта по референсу.

Даёт «форму» из картинки: bbox объекта, пропорции, площадь покрытия и грубую
маску силуэта. Используется, чтобы параметрическая модель повторяла пропорции
нарисованного объекта, а не только табличные габариты.

    python measure_ref.py --in ART_ASSETS/refs/trawler.png --out ART_ASSETS/models/_metrics/trawler.json
"""
import argparse
import json
import os
import sys
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
from PIL import Image

MASK_GRID = 96


def bg_model(rgb, ring=0.05):
    """Модель фона: на кадрах сильный виньет, поэтому цвет фона — не константа.

    Оцениваем гладкий фон как квадратичную функцию (x, y) по кольцу у краёв
    и вычитаем её из кадра — остаётся объект независимо от его тона.
    """
    h, w = rgb.shape[:2]
    band = max(4, int(min(h, w) * ring))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    xn, yn = xx / max(w - 1, 1), yy / max(h - 1, 1)
    edge = (xn < band / max(w - 1, 1)) | (xn > 1 - band / max(w - 1, 1)) | \
            (yn < band / max(h - 1, 1)) | (yn > 1 - band / max(h - 1, 1))
    idx = np.stack([np.ones_like(xn), xn, yn, xn * xn, yn * yn, xn * yn], axis=-1)
    A = idx[edge]
    model = np.empty_like(rgb, dtype=np.float64)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, rgb[:, :, c][edge].astype(np.float64), rcond=None)
        model[:, :, c] = idx @ coef
    return model


def mask_from(rgb, model, tol=62):
    diff = np.abs(rgb.astype(np.float64) - model).sum(axis=2)
    return diff > tol


def components(mask):
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    for sy in range(h):
        row = mask[sy]
        for sx in range(w):
            if not row[sx] or seen[sy, sx]:
                continue
            q = deque([(sy, sx)])
            seen[sy, sx] = True
            pts = []
            while q:
                y, x = q.popleft()
                pts.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            out.append(pts)
    return out


def measure(src, grid=MASK_GRID):
    im = Image.open(src).convert("RGB")
    rgb = np.asarray(im)
    model = bg_model(rgb)
    mask = mask_from(rgb, model)

    step = max(1, max(mask.shape) // 512)
    small = mask[::step, ::step]
    comps = components(small)
    if not comps:
        return {"source": src, "empty": True}
    comps.sort(key=len, reverse=True)
    pts = comps[0]
    ys = [p[0] for p in pts]
    xs = [p[1] for p in pts]
    y0, y1 = min(ys) * step, (max(ys) + 1) * step
    x0, x1 = min(xs) * step, (max(xs) + 1) * step
    bw, bh = x1 - x0, y1 - y0
    # крупные «хвосты» (линейка лежит отдельно) отбрасываем: оставляем bbox крупнейшей части
    other = [len(c) for c in comps[1:6]]

    # грубая маска силуэта внутри bbox (для сверки модели с картинкой)
    sub = mask[y0:y1, x0:x1]
    gh = max(1, min(grid, sub.shape[0]))
    gw = max(1, min(grid, sub.shape[1]))
    ysamp = np.linspace(0, sub.shape[0] - 1, gh).astype(int)
    xsamp = np.linspace(0, sub.shape[1] - 1, gw).astype(int)
    sil = sub[np.ix_(ysamp, xsamp)]
    silhouette = "".join("1" if v else "0" for v in sil.reshape(-1))

    return {
        "source": src,
        "image_px": [im.width, im.height],
        "bbox_px": [int(x0), int(y0), int(x1), int(y1)],
        "bbox_rel": [round(x0 / im.width, 4), round(y0 / im.height, 4),
                     round(x1 / im.width, 4), round(y1 / im.height, 4)],
        "object_px": [int(bw), int(bh)],
        "aspect_w_over_h": round(bw / max(bh, 1), 4),
        "coverage": round(len(pts) / max((small.shape[0] * small.shape[1]), 1), 4),
        "other_components": other,
        "silhouette_grid": [gw, gh],
        "silhouette": silhouette,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    args = ap.parse_args()
    info = measure(args.src)
    os.makedirs(os.path.dirname(os.path.abspath(args.dst)), exist_ok=True)
    with open(args.dst, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    print(f"{args.src} -> {args.dst}  aspect={info.get('aspect_w_over_h')} bbox={info.get('bbox_px')}")


if __name__ == "__main__":
    main()
