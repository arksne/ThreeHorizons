# -*- coding: utf-8 -*-
"""Ф2.9 · Blockout-прикидка масштаба квартала Аркенхольда (Blender EEVEE).

Строит квартал из `GAME_DESIGN/arkenhold_blocks.json` в натуральную величину:
1 м = 1 Blender-юнит. Рендерит 1600×900 в двух ракурсах — сверху и от глаз.

Запуск (только через обёртку — Blender без `--threads 2` ест CPU на 99 %):
    pwsh -File tools/blender.ps1 -Script blender/blockout.py

Выход: ART_ASSETS/blockout/arkenhold_top.png
        ART_ASSETS/blockout/arkenhold_eye.png
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GD = os.path.join(ROOT, "GAME_DESIGN")
OUT = os.path.join(ROOT, "ART_ASSETS", "blockout")

RENDER_W, RENDER_H = 1600, 900
EYE_H = 1.7          # рост человека (MASTER_SCALE_SPEC §2) — глаз камеры
WALL_H = 2.7         # жилой потолок

# материалы квартала: (цвет RGB, имя) — нейтральный блокаут, не финальный арт
MAT_GROUND = (0.42, 0.40, 0.36)
MAT_ROAD = (0.30, 0.29, 0.27)
MAT_BLOCK = (0.55, 0.53, 0.49)
MAT_ROOF = (0.35, 0.30, 0.26)
MAT_WATER = (0.25, 0.42, 0.48)
MAT_PERSON = (0.75, 0.25, 0.20)


def purge_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(coll):
            if item.users == 0:
                coll.remove(item)


def mat(name: str, rgb) -> bpy.types.Material:
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    return m


def box(name: str, x, y, z, sx, sy, sz, material):
    """Куб с центром (x, y, z) и размером (sx, sy, sz)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    ob = bpy.context.object
    ob.name = name
    ob.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(material)
    return ob


def build_city(data: dict):
    m_ground = mat("ground", MAT_GROUND)
    m_road = mat("road", MAT_ROAD)
    m_block = mat("block", MAT_BLOCK)
    m_roof = mat("roof", MAT_ROOF)
    m_water = mat("water", MAT_WATER)
    m_person = mat("person", MAT_PERSON)

    w, d = data["citySizeM"]
    grid = data["grid"]
    sm, ss = grid["streetMainM"], grid["streetSecondaryM"]

    # земля
    box("ground", w / 2, d / 2, -0.05, w + 40, d + 40, 0.1, m_ground)

    # вода — восточнее города (waterSide: east)
    box("water", w + 22, d / 2, -0.4, 44, d + 40, 0.2, m_water)

    # дороги: вертикальные по X-границам колонок, горизонтальная между рядами
    blocks = data["blocks"]
    cols = sorted({b["x"] for b in blocks})
    rows = sorted({b["z"] for b in blocks})
    for i, bx in enumerate(cols):
        if i == 0:
            continue
        street_w = sm if i in (1, 3) else ss
        box(f"road_v{i}", bx - street_w / 2, d / 2, 0.02, street_w, d, 0.04, m_road)
    if len(rows) > 1:
        box("road_h", w / 2, rows[1] - sm / 2, 0.02, w, sm, 0.04, m_road)

    # кварталы: земля квартала + здания вдоль улицы
    n_bldg = 0
    for blk in blocks:
        box(f"block_{blk['id']}", blk["x"] + blk["w"] / 2, blk["z"] + blk["d"] / 2,
            0.03, blk["w"], blk["d"], 0.06, m_road)
        for i, b in enumerate(blk.get("buildings", [])):
            cx = blk["x"] + b["x"] + b["w"] / 2
            cy = blk["z"] + b["z"] + b["d"] / 2
            h = 3.0 if b["kind"] in ("tavern", "warehouse", "workshop") else 2.7
            box(f"b_{blk['id']}_{i}", cx, cy, h / 2, b["w"], b["d"], h, m_block)
            # крыша — двускатная: два наклонных бруса + конёк
            box(f"r_{blk['id']}_{i}", cx, cy, h + 0.12, b["w"] + 0.3, b["d"] + 0.3, 0.24, m_roof)
            n_bldg += 1
        # причал
        dk = blk.get("dock")
        if dk:
            box("dock", blk["x"] + dk["x"] + dk["w"] / 2,
                blk["z"] + dk["z"] + dk["d"] / 2, 0.25, dk["w"], dk["d"], 0.5, m_roof)

    # улицы — отдельным слоем поверх, чтобы читались
    for s in data.get("streets", []):
        box(f"st_{s['id']}", s["x"] + s["w"] / 2, s["z"] + s["d"] / 2,
            0.05, s["w"], s["d"], 0.1, m_road)

    # фигура человека — эталон масштаба (1.7 м), стоит в главной улице перед камерой
    streets_h = [s for s in data.get("streets", []) if s["orientation"] == "horizontal"]
    main_h = max(streets_h, key=lambda s: s["d"])
    box("person", 22.0, main_h["z"] + main_h["d"] / 2, EYE_H / 2, 0.5, 0.35, EYE_H, m_person)
    return n_bldg


def setup_render() -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = RENDER_W
    scene.render.resolution_y = RENDER_H
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "Standard"

    # солнце
    sun_data = bpy.data.lights.new("sun", type="SUN")
    sun_data.energy = 3.0
    sun = bpy.data.objects.new("sun", sun_data)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    bpy.context.collection.objects.link(sun)

    # заполняющий свет
    area_data = bpy.data.lights.new("fill", type="AREA")
    area_data.energy = 8000
    area_data.size = 120
    area = bpy.data.objects.new("fill", area_data)
    area.location = (120, -160, 120)
    area.rotation_euler = (math.radians(55), 0, 0)
    bpy.context.collection.objects.link(area)

    world = bpy.data.worlds.new("w")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.60, 0.68, 1)
    scene.world = world


def camera(name: str, loc, look_at, lens=35) -> bpy.types.Object:
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam = bpy.data.objects.new(name, cam_data)
    cam.location = loc
    bpy.context.collection.objects.link(cam)
    track = cam.constraints.new("TRACK_TO")
    target = bpy.data.objects.new(name + "_target", None)
    target.location = look_at
    bpy.context.collection.objects.link(target)
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    return cam


def render(cam, path: str) -> None:
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main() -> None:
    data = json.loads(open(os.path.join(GD, "arkenhold_blocks.json"), encoding="utf-8").read())
    purge_scene()
    n = build_city(data)
    setup_render()
    os.makedirs(OUT, exist_ok=True)

    w, d = data["citySizeM"]

    # 1) сверху: весь город + вода в кадре
    cam_top = camera("cam_top", (w / 2, d / 2, 400), (w / 2, d / 2, 0), lens=36)
    render(cam_top, os.path.join(OUT, "arkenhold_top.png"))

    # 2) от глаз: стоим в главной горизонтальной улице (идёт вдоль X) и смотрим на восток.
    #    Слева — кварталы южного ряда, справа — северного; в кадре — фасады, улица, человек.
    streets_h = [s for s in data.get("streets", []) if s["orientation"] == "horizontal"]
    main_h = max(streets_h, key=lambda s: s["d"])
    road_y = main_h["z"] + main_h["d"] / 2
    cam_eye = camera("cam_eye", (6, road_y - 2, EYE_H), (w + 40, road_y + 6, 7), lens=30)
    render(cam_eye, os.path.join(OUT, "arkenhold_eye.png"))

    print(f"BLOCKOUT OK | зданий {n} | город {w}×{d} м | "
          f"{os.path.join(OUT, 'arkenhold_top.png')}, {os.path.join(OUT, 'arkenhold_eye.png')}")


if __name__ == "__main__":
    main()
