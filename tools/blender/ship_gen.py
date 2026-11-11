"""Параметрический генератор корпусов кораблей (код исполняется внутри Blender).

Лофтинг по станциям: полуширина, глубина киля и шерсть задаются кривыми,
сечение — суперэллипсом. На выходе — чистая низкополигональная сетка
(для Roblox) с палубой, фальшбортом, мачтами, рубкой и пушечными портами.

    from ship_gen import build_ship
    build_ship(spec, mats)
"""
import math

import bmesh
import bpy
from mathutils import Vector

TAU = math.pi * 2


# ---------------------------------------------------------------- утилиты
def purge_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for d in list(coll):
            if d.users == 0:
                coll.remove(d)


def srgb(hexv):
    """HEX -> линейный RGB (иначе цвета «горят»)."""
    hexv = hexv.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(hexv[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (out[0], out[1], out[2], 1.0)


def mat(name, hexv, rough=0.82, metal=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = srgb(hexv)
        bsdf.inputs["Roughness"].default_value = rough
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metal
    return m


def new_mesh_obj(name, verts, faces, material=None, collection=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    me.update()
    ob = bpy.data.objects.new(name, me)
    (collection or bpy.context.scene.collection).objects.link(ob)
    if material:
        ob.data.materials.append(material)
    # гладкие только по длинной стороне — торцы оставить плоскими
    for poly in me.polygons:
        poly.use_smooth = False
    recalc_normals(ob)
    return ob


def recalc_normals(ob):
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.update()


def merge_doubles(ob, dist=0.0005):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()


def add_box(name, center, size, material=None, rot=None):
    sx, sy, sz = (s / 2.0 for s in size)
    verts = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
             (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    ob = new_mesh_obj(name, verts, faces, material)
    ob.location = center
    if rot:
        ob.rotation_euler = rot
    return ob


def add_cylinder(name, p0, p1, r, material=None, seg=8):
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0)
    length = d.length
    if length < 1e-6:
        return None
    d.normalize()
    up = Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))
    u = d.cross(up).normalized()
    v = d.cross(u)
    verts, faces = [], []
    for i in range(seg):
        a = TAU * i / seg
        off = u * (math.cos(a) * r) + v * (math.sin(a) * r)
        verts.append(tuple(p0 + off))
        verts.append(tuple(p1 + off))
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
    faces.append(tuple(range(0, 2 * seg, 2))[::-1])
    faces.append(tuple(range(1, 2 * seg, 2)))
    return new_mesh_obj(name, verts, faces, material)


# ---------------------------------------------------------------- корпус
def hull_profile(t, p):
    """Полуширина корпуса: t=0 корма, t=1 нос."""
    x = abs(2 * t - 1)
    return max(0.0, (1.0 - x ** p)) ** 0.62


def keel_depth(t, flat=0.45, rise=2.6):
    """Глубина киля: плоское днище в средней части, подъём к носу/корме."""
    x = abs(2 * t - 1)
    if x <= flat:
        return 1.0
    return max(0.12, 1.0 - ((x - flat) / (1 - flat)) ** rise)


def sheer_height(t, freeboard, bow=0.16, stern=0.10):
    """Линия шерсти: выше у носа и кормы."""
    return freeboard * (1.0 + bow * (2 * t - 1) ** 2 * 2.0 + stern * (1 - t) ** 3)


def build_hull(spec, material):
    """spec: length, beam, depth, freeboard, fullness, stations, section_pts."""
    L = spec["length"]
    B = spec["beam"]
    D = spec["depth"]
    fb = spec["freeboard"]
    p = spec.get("fullness", 2.6)
    nst = spec.get("stations", 15)
    nsec = spec.get("section_pts", 7)
    rake = spec.get("stem_rake", 0.18)      # наклон носовой штевень
    stern = spec.get("stern", "round")       # round|square|transom|counter
    flat = spec.get("flat_bottom", 0.45)

    verts = []
    grid = []          # индексы вершин по станциям
    for si in range(nst):
        t = si / (nst - 1)
        hb = B / 2 * hull_profile(t, p)
        dz = D * keel_depth(t, flat)
        sh = sheer_height(t, fb, spec.get("sheer_bow", 0.16), spec.get("sheer_stern", 0.10))
        # смещение носа/кормы по X (штевень наклонён, корма с контр-штевнем)
        x = -L / 2 + L * t
        if stern == "counter" and t < 0.12:
            x += L * 0.06 * (1 - t / 0.12)
        row = []
        for si2 in range(nsec):
            f = si2 / (nsec - 1)
            # полуэллиптическое сечение: 0 = киль, 1 = планшир
            y = hb * math.sin(f * math.pi / 2) ** 0.78
            z = -dz * (1 - f) ** 1.35 + sh * f
            # полуразмах: зеркалим порты
            if si2 == 0:
                row.append(None)   # киль — один на обе стороны
            else:
                row.append(len(verts))
                verts.append((x, y, z))
        grid.append(row)

    # строим поверхность: для каждой станции формируем полный контур (левый+правый)
    faces = []
    rings = []
    for si in range(nst):
        t = si / (nst - 1)
        hb = B / 2 * hull_profile(t, p)
        dz = D * keel_depth(t, flat)
        sh = sheer_height(t, fb, spec.get("sheer_bow", 0.16), spec.get("sheer_stern", 0.10))
        x = -L / 2 + L * t
        if stern == "counter" and t < 0.12:
            x += L * 0.06 * (1 - t / 0.12)
        ring = []
        # правый борт снизу вверх
        for si2 in range(nsec):
            f = si2 / (nsec - 1)
            y = hb * math.sin(f * math.pi / 2) ** 0.78
            z = -dz * (1 - f) ** 1.35 + sh * f
            ring.append(len(verts))
            verts.append((x, y, z))
        # левый борт сверху вниз (без дубля киля и планшира)
        for si2 in range(nsec - 2, 0, -1):
            f = si2 / (nsec - 1)
            y = hb * math.sin(f * math.pi / 2) ** 0.78
            z = -dz * (1 - f) ** 1.35 + sh * f
            ring.append(len(verts))
            verts.append((x, -y, z))
        rings.append(ring)

    n = len(rings[0])
    for si in range(nst - 1):
        a, b = rings[si], rings[si + 1]
        for k in range(n - 1):
            faces.append((a[k], a[k + 1], b[k + 1], b[k]))
    # кормовые заглушки
    faces.append(tuple(rings[0]))
    faces.append(tuple(reversed(rings[-1])))
    ob = new_mesh_obj(spec.get("name", "hull"), verts, faces, material)
    merge_doubles(ob)
    return ob, rings, verts


def build_deck(spec, rings, verts, material):
    """Палуба: плоскость по линии планшира + фальшборт."""
    fb = spec["freeboard"]
    deck_z = fb * spec.get("deck_frac", 0.72)
    dh = []
    for ring in rings:
        row = []
        for idx in ring:
            x, y, z = verts[idx]
            row.append((x, y, deck_z))
        dh.append(row)
    n = len(dh[0])
    # берём половину контура (планшир) — палуба между правым и левым бортом
    half = n // 2 + 1
    verts2 = []
    idx2 = []
    for si, row in enumerate(dh):
        idxs = []
        for k in range(half):
            if k == 0:
                idxs.append(None)
            else:
                idxs.append(len(verts2))
                verts2.append(row[k])
        idx2.append(idxs)
    faces = []
    for si in range(len(dh) - 1):
        for k in range(half - 1):
            a0 = idx2[si][k]
            a1 = idx2[si][k + 1]
            b0 = idx2[si + 1][k]
            b1 = idx2[si + 1][k + 1]
            if None in (a0, a1, b0, b1):
                continue
            faces.append((a0, a1, b1, b0))
    deck = new_mesh_obj(spec.get("name", "hull") + "_deck", verts2, faces, material)

    bul = spec.get("bulwark", 0.0)
    if bul > 0:
        bv, bf = [], []
        for si, ring in enumerate(rings):
            pass
        # фальшборт: стенка по планширу наружу
        left = []
        for si, ring in enumerate(rings):
            x, y, z = verts[ring[half - 1]]
            left.append((x, y, z))
        right = []
        for si, ring in enumerate(rings):
            x, y, z = verts[ring[0]]
            right.append((x, y, z))
        wall_v, wall_f = [], []
        for i in range(len(rings)):
            x, y, z = left[i]
            wall_v.append((x, y, z))
            wall_v.append((x, y, z + bul))
        for i in range(len(rings) - 1):
            a = 2 * i
            wall_f.append((a, a + 1, a + 3, a + 2))
        bpy.app.driver_namespace["_bulwark_unused"] = wall_v
        bulwark = new_mesh_obj(spec.get("name", "hull") + "_bulwark", wall_v, wall_f, material)
        return deck, bulwark
    return deck, None


def build_ship(spec, mats):
    """Собирает корпус целиком: обшивка, палуба, фальшборт, мачты, надстройки."""
    name = spec.get("name", "ship")
    hull, rings, verts = build_hull(spec, mats["hull"])
    deck, bulwark = build_deck(spec, rings, verts, mats["deck"])
    parts = [hull, deck] + ([bulwark] if bulwark else [])

    L = spec["length"]
    B = spec["beam"]
    fb = spec["freeboard"]

    for i, m in enumerate(spec.get("masts", [])):
        x = -L / 2 + L * m.get("x", 0.5)
        base = fb * 0.8
        top = base + m.get("h", 6.0)
        parts.append(add_cylinder(f"{name}_mast{i}", (x, 0, base), (x, 0, top),
                                  m.get("r", 0.12), mats["wood"]))
        for y in m.get("yards", []):
            parts.append(add_box(f"{name}_yard{i}_{len(parts)}", (x, 0, top * y),
                                 (0.16, B * y, 0.14), mats["wood"]))

    cab = spec.get("cabin")
    if cab:
        x = -L / 2 + L * cab.get("x", 0.5)
        parts.append(add_box(f"{name}_cabin", (x, 0, fb * 0.9),
                             (cab.get("l", 1.6), cab.get("w", B * 0.5), cab.get("h", 0.8)),
                             mats["wood"]))

    for i, g in enumerate(spec.get("gunports", [])):
        x = -L / 2 + L * g.get("x", 0.5)
        for s in (-1, 1):
            parts.append(add_box(f"{name}_port{i}{'p' if s > 0 else 's'}",
                                 (x, s * (B / 2 - 0.05), fb * g.get("z", 0.55)),
                                 (g.get("w", 0.28), 0.08, g.get("h", 0.22)), mats["iron"]))

    # сдвигаем всё в начало координат по X и ставим киль на Z=0
    for ob in parts:
        ob.location.x -= L / 2
        for v in ob.data.vertices:
            v.co.z += D_of(spec)
    return parts, spec


def D_of(spec):
    return spec["depth"]
