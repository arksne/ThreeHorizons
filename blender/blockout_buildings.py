# -*- coding: utf-8 -*-
"""Ф4 · 3D-блокаут зданий по данным (Blender EEVEE).

Строит здания из `GAME_DESIGN/Buildings.json` в натуральную величину (1 м = 1 юнит)
и рендерит лист-эталон: 3/4, фасад, бок — как у референсов в `ART_ASSETS/refs/`.

Ключевое: материалы не «блоки», а процедурная кладка и черепица (ноды Brick),
конструкция читается: цоколь, фахверк с раскосами, окна в рамах с переплётом и отливом,
дверь с петлями, свес кровли, конёк, труба с колпаком.

Запуск: pwsh -File tools/blender.ps1 -Script blender/blockout_buildings.py
Выход: ART_ASSETS/visual_library/buildings/<id>_{34,front,side}.png
"""
import json
import math
import os

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GD = os.path.join(ROOT, "GAME_DESIGN")
OUT = os.path.join(ROOT, "ART_ASSETS", "visual_library", "buildings")

RENDER_W, RENDER_H = 1100, 850
EYE_H = 1.7
FLOOR_H = 2.7
DOOR_W, DOOR_H = 1.0, 2.1
WIN_W, WIN_H = 0.9, 1.1
BEAM = 0.22          # сечение фахверка
PLINTH_H = 0.45      # цоколь


# ------------------------------------------------------------------ материалы
def srgb(hexv):
    h = hexv.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out


def _mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def masonry(name, base, mortar, scale=6.0, rough=0.92, bump=0.25):
    """Процедурная каменная кладка: Brick Texture + шум + рельеф шва."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]

    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.5
    brick.offset_frequency = 2
    brick.squash = 1.0
    brick.squash_frequency = 2
    brick.inputs["Color1"].default_value = (*base, 1)
    brick.inputs["Color2"].default_value = (*_mix(base, mortar, 0.35), 1)
    brick.inputs["Mortar"].default_value = (*mortar, 1)
    brick.inputs["Scale"].default_value = scale
    brick.inputs["Mortar Size"].default_value = 0.018
    brick.inputs["Mortar Smooth"].default_value = 0.25
    brick.inputs["Bias"].default_value = 0.0
    brick.inputs["Brick Width"].default_value = 0.62
    brick.inputs["Row Height"].default_value = 0.28

    # лёгкий разброс цвета камней
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale * 4.0
    noise.inputs["Detail"].default_value = 3.0
    mixn = nt.nodes.new("ShaderNodeMixRGB")
    mixn.blend_type = "MULTIPLY"
    mixn.inputs["Fac"].default_value = 0.22
    nt.links.new(brick.outputs["Color"], mixn.inputs["Color1"])
    nt.links.new(noise.outputs["Color"], mixn.inputs["Color2"])
    nt.links.new(mixn.outputs["Color"], bsdf.inputs["Base Color"])

    # рельеф: швы глубже
    bmp = nt.nodes.new("ShaderNodeBump")
    bmp.inputs["Strength"].default_value = bump
    bmp.inputs["Distance"].default_value = 0.04
    nt.links.new(brick.outputs["Fac"], bmp.inputs["Height"])
    nt.links.new(bmp.outputs["Normal"], bsdf.inputs["Normal"])

    bsdf.inputs["Roughness"].default_value = rough
    return m


def tiles(name, base, mortar, scale=9.0, rough=0.62, bump=0.5):
    """Черепица: Brick Texture со сдвигом рядов (вполоска) + сильный рельеф."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]

    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.5
    brick.offset_frequency = 2
    brick.inputs["Color1"].default_value = (*base, 1)
    brick.inputs["Color2"].default_value = (*_mix(base, mortar, 0.5), 1)
    brick.inputs["Mortar"].default_value = (*mortar, 1)
    brick.inputs["Scale"].default_value = scale
    brick.inputs["Mortar Size"].default_value = 0.006
    brick.inputs["Mortar Smooth"].default_value = 0.05
    brick.inputs["Bias"].default_value = 0.0
    brick.inputs["Brick Width"].default_value = 0.34
    brick.inputs["Row Height"].default_value = 0.20

    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 30.0
    mixn = nt.nodes.new("ShaderNodeMixRGB")
    mixn.blend_type = "MULTIPLY"
    mixn.inputs["Fac"].default_value = 0.18
    nt.links.new(brick.outputs["Color"], mixn.inputs["Color1"])
    nt.links.new(noise.outputs["Color"], mixn.inputs["Color2"])
    nt.links.new(mixn.outputs["Color"], bsdf.inputs["Base Color"])

    bmp = nt.nodes.new("ShaderNodeBump")
    bmp.inputs["Strength"].default_value = bump
    bmp.inputs["Distance"].default_value = 0.05
    nt.links.new(brick.outputs["Fac"], bmp.inputs["Height"])
    nt.links.new(bmp.outputs["Normal"], bsdf.inputs["Normal"])

    bsdf.inputs["Roughness"].default_value = rough
    return m


def plain(name, hexv, rough=0.85, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*srgb(hexv), 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def wood(name, hexv, rough=0.8):
    """Дерево: волокна полосами вдоль длины."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "BANDS"
    wave.bands_direction = "Z"
    wave.inputs["Scale"].default_value = 22.0
    wave.inputs["Distortion"].default_value = 6.0
    wave.inputs["Detail"].default_value = 3.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    c = srgb(hexv)
    ramp.color_ramp.elements[0].color = (*_mix(c, (0, 0, 0), 0.45), 1)
    ramp.color_ramp.elements[1].color = (*c, 1)
    nt.links.new(wave.outputs["Color"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    return m


# ------------------------------------------------------------------ геометрия
def purge():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(coll):
            if item.users == 0:
                coll.remove(item)


def box(name, cx, cy, cz, sx, sy, sz, material, rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    ob = bpy.context.object
    ob.name = name
    ob.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if rot:
        ob.rotation_euler = rot
    ob.data.materials.append(material)
    return ob


def beam(name, p0, p1, thick, material):
    """Брус между двумя точками (для раскосов фахверка)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    L = d.length
    ob = box(name, 0, 0, 0, thick, thick, L, material)
    ob.location = (p0 + p1) / 2
    ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return ob


def gable_roof(name, cx, cy, z0, w, d, h, material, overhang=0.35):
    """Двускатная крыша с коньком и свесами."""
    hw, hd = w / 2, d / 2
    base = [(-hw, -hd, 0), (hw, -hd, 0), (hw, hd, 0), (-hw, hd, 0)]
    ridge = [(0, -hd, h), (0, hd, h)]
    faces = [(0, 1, 2, 3), (0, 1, 4), (3, 2, 5), (0, 3, 5, 4), (1, 2, 5, 4)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(base + ridge, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.location = (cx, cy, z0)
    ob.data.materials.append(material)
    bpy.context.collection.objects.link(ob)
    # свесы (доски вдоль карнизов)
    box(name + "_eaveA", cx, cy - hd - 0.04, z0 + 0.03, w + 0.12, 0.16, 0.10, material)
    box(name + "_eaveB", cx, cy + hd + 0.04, z0 + 0.03, w + 0.12, 0.16, 0.10, material)
    # конёк
    box(name + "_ridge", cx, cy, z0 + h + 0.05, 0.34, d + 0.1, 0.16, material)
    return ob


def window_set(name, cx, cy, cz, w, h, mats, facing="front"):
    """Окно: проём (тёмный), рама, переплёт крест-накрест, отлив."""
    depth = 0.14
    box(name + "_void", cx, cy + depth * 0.25, cz, w, 0.06, h, mats["glass"])
    t = 0.07
    box(name + "_f1", cx - w / 2, cy, cz, t, 0.1, h + t, mats["timber"])
    box(name + "_f2", cx + w / 2, cy, cz, t, 0.1, h + t, mats["timber"])
    box(name + "_f3", cx, cy, cz + h / 2, w + t, 0.1, t, mats["timber"])
    box(name + "_f4", cx, cy, cz - h / 2, w + t, 0.1, t, mats["timber"])
    box(name + "_mv", cx, cy, cz, 0.06, 0.09, h, mats["timber"])
    box(name + "_mh", cx, cy, cz, w, 0.09, 0.06, mats["timber"])
    # отлив (каменный подоконник)
    box(name + "_sill", cx, cy - 0.06, cz - h / 2 - 0.08, w + 0.34, 0.2, 0.12, mats["stone_light"])


def door_set(name, cx, cy, cz, mats):
    """Дверь: тёмный проём, полотно с досками, петли, кольцо."""
    box(name + "_void", cx, cy + 0.08, cz / 2, DOOR_W, 0.08, DOOR_H, mats["dark"])
    box(name + "_leaf", cx, cy, cz / 2, DOOR_W - 0.08, 0.1, DOOR_H - 0.05, mats["timber"])
    for z in (cz * 0.28, cz * 0.74):
        box(name + "_hinge", cx - DOOR_W / 2 + 0.06, cy - 0.06, z, 0.3, 0.05, 0.07, mats["iron"])
    # кольцо
    bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.022,
                                     location=(cx + DOOR_W * 0.28, cy - 0.1, cz * 0.52),
                                     rotation=(math.radians(90), 0, 0))
    ring = bpy.context.object
    ring.name = name + "_ring"
    ring.data.materials.append(mats["iron"])
    # косяк
    box(name + "_jambL", cx - DOOR_W / 2 - 0.06, cy, cz / 2, 0.12, 0.14, DOOR_H, mats["timber"])
    box(name + "_jambR", cx + DOOR_W / 2 + 0.06, cy, cz / 2, 0.12, 0.14, DOOR_H, mats["timber"])
    box(name + "_lintel", cx, cy, cz + DOOR_H / 2 + 0.07, DOOR_W + 0.3, 0.16, 0.14, mats["timber"])


def half_timber(name, w, d, floors, mats, door_x=0.32):
    """Фахверк: цокольная балка, стойки, обвязка этажей, раскосы, щипцы."""
    y_front = -d / 2 - 0.06
    y_back = d / 2 + 0.06
    n = max(2, int(round(w / 2.6)))

    # обвязка этажей: низ (цокольная) и верх каждого этажа
    for f in range(floors + 1):
        z = PLINTH_H + f * FLOOR_H
        box(f"{name}_band_f{f}", w / 2, y_front, z, w + 0.08, 0.16, BEAM, mats["timber"])
        box(f"{name}_bandb_f{f}", w / 2, y_back, z, w + 0.08, 0.16, BEAM, mats["timber"])
        # угловые стойки
        for s in (0.0, w):
            box(f"{name}_cpost_f{f}_{s}", s, y_front, z + FLOOR_H / 2,
                BEAM, 0.16, FLOOR_H, mats["timber"])

    # вертикальные стойки на фасаде (кроме угла) + раскосы
    for i in range(1, n):
        x = w * i / n
        for f in range(floors):
            z0 = PLINTH_H + f * FLOOR_H
            box(f"{name}_post_f{f}_{i}", x, y_front, z0 + FLOOR_H / 2,
                BEAM, 0.14, FLOOR_H, mats["timber"])
            # раскос: снизу-влево → вверх-вправо (как в референсе)
            beam(f"{name}_brace_f{f}_{i}",
                 (x - w / n / 2, y_front - 0.01, z0 + 0.25),
                 (x + w / n / 2, y_front - 0.01, z0 + FLOOR_H - 0.25),
                 BEAM * 0.85, mats["timber"])

    # щипцы: центральная стойка + раскосы к коньку
    ztop = PLINTH_H + floors * FLOOR_H
    roof_h = min(2.8, w * 0.30)
    box(f"{name}_gpost", w / 2, y_front, ztop + roof_h / 2, BEAM, 0.14, roof_h, mats["timber"])
    for sgn in (-1, 1):
        beam(f"{name}_gbrace{sgn}",
             (w / 2 + sgn * w * 0.16, y_front - 0.01, ztop + 0.12),
             (w / 2, y_front - 0.01, ztop + roof_h - 0.12),
             BEAM * 0.8, mats["timber"])
    return ztop, roof_h


def chimney(name, x, y, z_base, z_top, mats, cap=True):
    box(name, x, y, (z_base + z_top) / 2, 0.72, 0.72, z_top - z_base, mats["stone"])
    if cap:
        box(name + "_cap", x, y, z_top + 0.08, 0.9, 0.9, 0.16, mats["stone_light"])


def build_house(spec, mats):
    """Обычный дом с фахверком."""
    w, d = spec["sizeM"]
    fl = spec.get("floors", 2)
    floors = max(fl) if isinstance(fl, (list, tuple)) else int(fl)

    # цоколь
    box("plinth", w / 2, 0, PLINTH_H / 2, w + 0.22, d + 0.22, PLINTH_H, mats["stone_light"])
    # тело
    body_h = floors * FLOOR_H
    box("body", w / 2, 0, PLINTH_H + body_h / 2, w, d, body_h, mats["stone"])

    ztop, roof_h = half_timber("ht", w, d, floors, mats)

    # крыша с ориентацией конька вдоль длинной стороны
    if w >= d:
        gable_roof("roof", w / 2, 0, ztop, w + 0.7, d + 0.7, roof_h, mats["roof"])
    else:
        gable_roof("roof", w / 2, 0, ztop, d + 0.7, w + 0.7, roof_h, mats["roof"])
        # при коньке вдоль Y разворачиваем примитив
        for ob in bpy.data.objects:
            if ob.name == "roof":
                ob.rotation_euler.z = math.radians(90)

    # проёмы
    door_x = w * 0.32
    door_set("door", door_x, -d / 2 - 0.02, PLINTH_H, mats)
    for f in range(floors):
        z = PLINTH_H + f * FLOOR_H + 1.35
        n = max(2, int(round(w / 2.6)))
        for i in range(n + 1):
            x = w * i / n
            if abs(x - door_x) < 0.95 and f == 0:
                continue
            window_set(f"win{f}_{i}", x, -d / 2 - 0.04, z, WIN_W, WIN_H, mats)
    # на боковой стене — одно окно
    window_set("winside", -w / 2 - 0.04, 0, PLINTH_H + 1.35, WIN_W, WIN_H, mats)
    box("winside_rot", 0, 0, 0, 0.01, 0.01, 0.01, mats["dark"])   # заглушка

    # труба
    chimney("chimney", w * 0.78, d * 0.18, ztop - 0.4, ztop + roof_h + 1.3, mats)
    return w, d, ztop + roof_h + 1.5


def build_tower(spec, mats):
    w, d = spec["sizeM"]
    h = FLOOR_H * 3
    box("plinth", w / 2, 0, PLINTH_H / 2, w + 0.24, d + 0.24, PLINTH_H, mats["stone_light"])
    box("body", w / 2, 0, PLINTH_H + h / 2, w, d, h, mats["stone"])
    # вынесенный верх
    top_z = PLINTH_H + h
    box("top", w / 2, 0, top_z + 0.8, w + 0.7, d + 0.7, 1.6, mats["stone"])
    roof_h = 1.7
    gable_roof("roof", w / 2, 0, top_z + 1.6, w + 1.0, d + 1.0, roof_h, mats["roof"])
    # часы
    box("clock", w / 2, -d / 2 - 0.06, top_z - 1.4, 1.0, 0.14, 1.0, mats["trim"])
    box("clockhand", w / 2, -d / 2 - 0.14, top_z - 1.4, 0.06, 0.04, 0.5, mats["iron"])
    # окна
    for f in range(3):
        z = PLINTH_H + f * FLOOR_H + 1.35
        window_set(f"win{f}", w / 2, -d / 2 - 0.04, z, 0.7, 1.3, mats)
    chimney("chimney", w * 0.3, d * 0.2, top_z - 0.3, top_z + roof_h + 1.4, mats)
    return w + 1.0, d + 1.0, top_z + 1.6 + roof_h + 1.5


def build_manor(spec, mats):
    w, d = spec["sizeM"]
    floors = 2
    body_w = w - 3.4
    box("plinth", body_w / 2 + 1.2, 0, PLINTH_H / 2, body_w + 0.24, d + 0.24, PLINTH_H, mats["stone_light"])
    box("body", body_w / 2 + 1.2, 0, PLINTH_H + floors * FLOOR_H / 2,
        body_w, d, floors * FLOOR_H, mats["stone"])
    ztop = PLINTH_H + floors * FLOOR_H
    # угловая башня
    tx, ts = w - 2.6, 3.4
    th = ztop + 2.4
    box("tower", tx, 0, th / 2, ts, ts, th, mats["stone"])
    box("towerband", tx, 0, th - 0.5, ts + 0.3, ts + 0.3, 0.3, mats["timber"])
    gable_roof("towerroof", tx, 0, th, ts + 0.7, ts + 0.7, 2.1, mats["roof"])
    # портик
    px, pd = 4.0, d / 2 + 1.2
    for i in range(4):
        x = 1.2 + i * 1.5
        box(f"col{i}", x, -pd, 1.7, 0.38, 0.38, 3.4, mats["stone_light"])
    box("porch", 3.4, -pd, 3.55, 6.6, 1.9, 0.42, mats["roof"])
    # крыша дома
    roof_h = 2.6
    gable_roof("roof", body_w / 2 + 1.2, 0, ztop, body_w + 0.7, d + 0.7, roof_h, mats["roof"])
    door_set("door", 3.4, -d / 2 - 0.02, PLINTH_H, mats)
    for f in range(floors):
        for i in range(3):
            x = 2.0 + i * 2.6
            window_set(f"win{f}_{i}", x, -d / 2 - 0.04, PLINTH_H + f * FLOOR_H + 1.35,
                       WIN_W, WIN_H, mats)
    chimney("chimney", body_w + 0.6, d * 0.2, ztop - 0.3, ztop + roof_h + 1.3, mats)
    return w, d, th + 2.4


def build_warehouse(spec, mats):
    w, d = spec["sizeM"]
    h = FLOOR_H * 2 + 1.2
    box("plinth", w / 2, 0, PLINTH_H / 2, w + 0.2, d + 0.2, PLINTH_H, mats["stone_light"])
    box("body", w / 2, 0, PLINTH_H + (h - PLINTH_H) / 2, w, d, h - PLINTH_H, mats["stone"])
    # плоская кровля с парапетом
    box("parapetA", w / 2, -d / 2, h + 0.25, w + 0.3, 0.3, 0.5, mats["stone"])
    box("parapetB", w / 2, d / 2, h + 0.25, w + 0.3, 0.3, 0.5, mats["stone"])
    box("parapetC", 0, 0, h + 0.25, 0.3, d + 0.3, 0.5, mats["stone"])
    box("parapetD", w, 0, h + 0.25, 0.3, d + 0.3, 0.5, mats["stone"])
    box("roof", w / 2, 0, h + 0.05, w, d, 0.12, mats["timber"])
    # слуховые люки
    for i in range(2):
        x = w * (0.3 + i * 0.4)
        box(f"dormer{i}", x, 0, h + 0.7, 1.8, 1.6, 1.3, mats["stone"])
        box(f"dormerroof{i}", x, 0, h + 1.4, 2.0, 1.8, 0.3, mats["roof"])
    # большие ворота с филёнками
    for s in (-1, 1):
        x = w / 2 + s * w * 0.22
        box(f"gate{s}", x, -d / 2 - 0.05, PLINTH_H + 1.6, 3.0, 0.12, 3.2, mats["timber"])
        for k in range(5):
            box(f"gatepanel{s}_{k}", x - 1.2 + k * 0.6, -d / 2 - 0.11, PLINTH_H + 1.6,
                0.08, 0.06, 3.0, mats["timber"])
    return w, d, h + 1.6


def build_dock(spec, mats):
    w, d = spec["sizeM"]
    box("deck", w / 2, 0, 0.35, w, d, 0.4, mats["timber"])
    n = int(w / 3.2)
    for i in range(n):
        x = (i + 0.5) * w / n
        for s in (-1, 1):
            box(f"pile{i}{s}", x, s * (d / 2 - 0.5), -1.1, 0.42, 0.42, 2.6, mats["timber"])
    # перила
    for s in (-1, 1):
        box(f"rail{s}", w / 2, s * (d / 2 - 0.15), 1.15, w, 0.12, 0.12, mats["timber"])
        for i in range(int(w / 2.5) + 1):
            x = i * 2.5
            box(f"post{s}_{i}", x, s * (d / 2 - 0.15), 0.85, 0.12, 0.12, 0.9, mats["timber"])
    # тумбы
    for i in range(int(w / 8)):
        x = 3.0 + i * 8.0
        box(f"bollard{i}", x, -(d / 2 - 0.9), 0.95, 0.42, 0.42, 1.2, mats["trim"])
    # фонарь
    box("lamppost", w - 3.0, 0, 1.9, 0.24, 0.24, 3.4, mats["trim"])
    box("lamp", w - 3.0, 0, 3.75, 0.5, 0.5, 0.7, mats["glass"])
    return w, d, 4.2


def build_wall(spec, mats):
    L, h, t = 10.0, 2.0, 1.0
    box("wall", L / 2, 0, h / 2, L, t, h, mats["stone"])
    n = 8
    for i in range(n):
        x = 0.5 + i * (L - 1.0) / (n - 1)
        box(f"merlon{i}", x, 0, h + 0.3, 0.72, t + 0.1, 0.6, mats["stone"])
    box("walk", L / 2, 0, h + 0.04, L, t + 0.35, 0.1, mats["timber"])
    return L, t, h + 0.6


def build_gate(spec, mats):
    h = 4.2
    for s in (-1, 1):
        box(f"pier{s}", 2.0 + s * 2.3, 0, h / 2, 1.1, 1.3, h, mats["stone"])
        box(f"piercap{s}", 2.0 + s * 2.3, 0, h + 0.15, 1.4, 1.6, 0.3, mats["stone_light"])
    box("lintel", 0, 0, h - 0.45, 5.8, 1.3, 0.9, mats["stone"])
    box("doors", 0, 0, 1.7, 3.5, 0.3, 3.4, mats["timber"])
    for k in range(6):
        box(f"dp{k}", -1.5 + k * 0.6, -0.2, 1.7, 0.08, 0.08, 3.3, mats["timber"])
    return 6.8, 1.3, h + 0.3


BUILDERS = {
    "house_small": build_house, "house_medium": build_house, "house_large": build_house,
    "shop": build_house, "tavern": build_house, "workshop": build_house,
    "warehouse": build_warehouse, "dock": build_dock,
}


# ------------------------------------------------------------------ рендер
def setup_render():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.render.resolution_x = RENDER_W
    sc.render.resolution_y = RENDER_H
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"

    sun_d = bpy.data.lights.new("sun", type="SUN")
    sun_d.energy = 2.4
    sun_d.angle = math.radians(14)
    sun = bpy.data.objects.new("sun", sun_d)
    sun.rotation_euler = (math.radians(52), 0, math.radians(38))
    bpy.context.collection.objects.link(sun)

    fill_d = bpy.data.lights.new("fill", type="AREA")
    fill_d.energy = 12000
    fill_d.size = 120
    fill = bpy.data.objects.new("fill", fill_d)
    fill.location = (-70, -130, 100)
    fill.rotation_euler = (math.radians(58), 0, 0)
    bpy.context.collection.objects.link(fill)

    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.52, 0.53, 0.55, 1)
    sc.world = w


def cam(name, loc, look, lens=40):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    c = bpy.data.objects.new(name, cd)
    c.location = loc
    bpy.context.collection.objects.link(c)
    tr = c.constraints.new("TRACK_TO")
    t = bpy.data.objects.new(name + "_t", None)
    t.location = look
    bpy.context.collection.objects.link(t)
    tr.target = t
    tr.track_axis = "TRACK_NEGATIVE_Z"
    tr.up_axis = "UP_Y"
    return c


def make_materials():
    return {
        "stone": masonry("masonry", srgb("#8A8578"), srgb("#6E6A5F"), scale=5.0),
        "stone_light": masonry("masonry_light", srgb("#A9A496"), srgb("#8A8578"), scale=7.0),
        "roof": tiles("tiles", srgb("#2B2E33"), srgb("#1A1C1F"), scale=7.0),
        "timber": wood("timber", "#4A3226"),
        "trim": wood("trim", "#6B4A2E"),
        "glass": plain("glass", "#9AA2A8", rough=0.25, metal=0.1),
        "dark": plain("dark", "#14161A", rough=0.9),
        "iron": plain("iron", "#2A2C30", rough=0.5, metal=0.75),
        "ground": plain("ground", "#B8BEB4", rough=0.95),
        "person": plain("person", "#8C2B1B", rough=0.9),
    }


def human(mats):
    """Фигура человека 1.7 м — эталон масштаба."""
    box("h_legs", 0, 0, 0.42, 0.44, 0.30, 0.84, mats["person"])
    box("h_torso", 0, 0, 1.15, 0.50, 0.32, 0.62, mats["person"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=(0, 0, 1.58))
    head = bpy.context.object
    head.name = "h_head"
    head.data.materials.append(mats["person"])


def main():
    specs = json.loads(open(os.path.join(GD, "Buildings.json"), encoding="utf-8").read())["classes"]
    os.makedirs(OUT, exist_ok=True)

    for spec in specs:
        purge()
        setup_render()
        fid = spec["id"]
        ref_id = "bld_" + fid if not fid.startswith("bld_") else fid
        mats = make_materials()

        if fid == "bld_tower":
            w, d, h = build_tower(spec, mats)
        elif fid == "bld_manor":
            w, d, h = build_manor(spec, mats)
        elif fid == "bld_wall":
            w, d, h = build_wall(spec, mats)
        elif fid == "bld_gate":
            w, d, h = build_gate(spec, mats)
        elif fid == "bld_dock":
            w, d, h = build_dock(spec, mats)
        else:
            w, d, h = build_house(spec, mats)

        box("ground", w / 2, 0, -0.07, w * 4, d * 4, 0.14, mats["ground"])
        human(mats)

        span = max(w, d, h) * 1.5
        for tag, loc, look, lens in (
            ("34", (w / 2 - span * 0.85, -span * 1.05, h * 0.62 + span * 0.30),
             (w / 2, 0, h * 0.40), 38),
            ("front", (w / 2, -span * 1.55, h * 0.38), (w / 2, 0, h * 0.38), 50),
            ("side", (-span * 1.55, 0, h * 0.38), (0, 0, h * 0.38), 50),
        ):
            c = cam("c_" + tag, loc, look, lens=lens)
            bpy.context.scene.camera = c
            bpy.context.scene.render.filepath = os.path.join(OUT, f"{ref_id}_{tag}.png")
            bpy.ops.render.render(write_still=True)

        print(f"BLOCKOUT OK {ref_id}: {w:.1f}x{d:.1f} h={h:.1f}")

    print(f"BLOCKOUT DONE: {len(specs)} зданий → {OUT}")


if __name__ == "__main__":
    main()
