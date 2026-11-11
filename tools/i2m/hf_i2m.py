"""Image-to-3D через Hugging Face Spaces (Hunyuan3D-2.1 / Stable Fast 3D).

Машина без NVIDIA GPU, поэтому нейросети крутятся в ZeroGPU-пространствах HF.
Модуль: грузит референс, гонит в Space, забирает GLB/OBJ + текстуру.

    python hf_i2m.py --image refs/trawler.png --out out/trawler
    python hf_i2m.py --image ... --out ... --backend sf3d
"""
import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BACKENDS = {
    "hunyuan": {
        "space": "tencent/Hunyuan3D-2-1",
        "host": "tencent-Hunyuan3D-2-1.hf.space",
        "generate": "/generation_all",
        "export": "/on_export_click",
    },
    "sf3d": {
        "space": "stabilityai/stable-fast-3d",
        "host": "stabilityai-stable-fast-3d.hf.space",
        "generate": "/run_button",
        "export": None,
    },
}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def connect(host, token=None):
    from gradio_client import Client
    kwargs = {"hf_token": token} if token else {}
    url = host if host.startswith("http") else f"https://{host}"
    log(f"connecting to {url} ...")
    return Client(url, verbose=False, **kwargs)


def download_all(gr, out_dir):
    """Скачивает все файлы, которые вернул Gradio (модель + текстуры)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for f in gr.download_all():
        dest = out_dir / Path(f.name).name
        shutil.copy(f, dest)
        saved.append(str(dest))
        log(f"  saved {dest.name} ({dest.stat().st_size} bytes)")
    return saved


def run_hunyuan(gr, image_path, steps=30, guidance=3.5, octree=256, texture=True,
                simplify=True, target_faces=60000, file_type="glb"):
    api = gr.predict
    log(f"generation_all: steps={steps} guidance={guidance} octree={octree}")
    res = api(
        image=image_path,
        mv_image_front=None,
        mv_image_back=None,
        mv_image_left=None,
        mv_image_right=None,
        steps=steps,
        guidance_scale=guidance,
        seed=-1,
        octree_resolution=octree,
        check_box_rembg=True,
        num_chunks=1,
        randomize_seed=True,
        api_name="/generation_all",
    )
    log(f"generation_all -> {type(res)}")
    shape_file = None
    for r in (res if isinstance(res, (list, tuple)) else [res]):
        if hasattr(r, "name") and str(r.name).lower().endswith((".glb", ".ply", ".obj")):
            shape_file = r
            break
    if shape_file is None:
        shape_file = res if isinstance(res, (str, type(None))) else (res[0] if isinstance(res, (list, tuple)) and res else None)
    if shape_file is None:
        raise RuntimeError("Hunyuan3D не вернул файл")

    log("export (glb, текстуры, simplification)")
    try:
        exp = api(
            "/on_export_click",
            file_out=shape_file,
            file_out2=None,
            file_type=file_type,
            reduce_face=simplify,
            export_texture=texture,
            target_face_num=target_faces,
            api_name="/on_export_click",
        )
        return exp
    except Exception as e:
        log(f"export failed ({e}); верну shape напрямую")
        return shape_file


def run_sf3d(gr, image_path, vertex_count=10000, texture_size=1024, foreground_ratio=0.3,
             remesh="None"):
    res = gr.predict(
        input_image=image_path,
        foreground_ratio=foreground_ratio,
        remesh_option=remesh,
        vertex_count=vertex_count,
        texture_size=texture_size,
        api_name="/run_button",
    )
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--backend", default="hunyuan", choices=list(BACKENDS))
    ap.add_argument("--token", default=os.environ.get("HF_TOKEN", ""))
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--guidance", type=float, default=3.5)
    ap.add_argument("--octree", type=int, default=256)
    ap.add_argument("--target-faces", type=int, default=60000)
    ap.add_argument("--vertex-count", type=int, default=10000)
    ap.add_argument("--texture-size", type=int, default=1024)
    ap.add_argument("--file-type", default="glb")
    args = ap.parse_args()

    cfg = BACKENDS[args.backend]
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    gr = connect(cfg["host"], args.token or None)
    t0 = time.time()
    if args.backend == "hunyuan":
        res = run_hunyuan(gr, args.image, steps=args.steps, guidance=args.guidance,
                          octree=args.octree, target_faces=args.target_faces,
                          file_type=args.file_type)
    else:
        res = run_sf3d(gr, args.image, vertex_count=args.vertex_count,
                       texture_size=args.texture_size)

    saved = download_all(gr, out_dir)
    meta = {"backend": args.backend, "space": cfg["space"], "image": args.image,
            "seconds": round(time.time() - t0, 1), "files": saved}
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"готово за {meta['seconds']}s -> {out_dir}")
    if not saved:
        log("WARNING: ни одного файла не скачано")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
