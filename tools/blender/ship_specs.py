"""Параметры 20 корпусов Three Horizons.

Размеры — из model-classes.json / subjects.json (notes: "hull L x B m, freeboard H m"),
профиль — по промптам референсов (острый/пузатый нос, тип кормы, мачты, пушечные ряды).

Длина/ширина в метрах, глубина корпуса = 1.35 * freeboard (скорость + осадка),
высота мачт — доля от длины.
"""


def _spec(length, beam, freeboard, **kw):
    d = {
        "length": length,
        "beam": beam,
        "freeboard": freeboard,
        "depth": round(freeboard * 1.35, 2),
        "fullness": 2.8,
        "stations": 15,
        "section_pts": 7,
        "sheer_bow": 0.16,
        "sheer_stern": 0.10,
        "deck_frac": 0.72,
        "bulwark": 0.0,
        "flat_bottom": 0.45,
        "stern": "counter",
        "masts": [],
        "gunports": [],
        "cabin": None,
    }
    d.update(kw)
    return d


SHIPS = {
    "skiff": _spec(4.0, 1.5, 0.8, fullness=2.2, flat_bottom=0.62, stern="square",
                   deck_frac=0.5, sheer_bow=0.08, sheer_stern=0.06),
    "trawler": _spec(7.0, 2.5, 1.0, fullness=2.6, flat_bottom=0.5, stern="transom",
                     deck_frac=0.7, sheer_bow=0.12, sheer_stern=0.10,
                     cabin={"x": 0.62, "l": 1.2, "w": 1.1, "h": 0.7}),
    "sloop": _spec(10.0, 3.5, 1.2, fullness=2.9, stern="counter", sheer_bow=0.16,
                   sheer_stern=0.12,
                   masts=[{"x": 0.42, "h": 5.5, "r": 0.09}],
                   cabin={"x": 0.62, "l": 1.6, "w": 1.5, "h": 0.6}),
    "cutter": _spec(14.0, 4.5, 1.4, fullness=3.3, stern="transom", sheer_bow=0.20,
                    sheer_stern=0.08,
                    masts=[{"x": 0.44, "h": 8.0, "r": 0.10}]),
    "smack": _spec(12.0, 3.2, 1.1, fullness=2.2, stern="transom", sheer_bow=0.18,
                   sheer_stern=0.12, deck_frac=0.66, bulwark=0.28,
                   masts=[{"x": 0.30, "h": 6.5, "r": 0.09}]),
    "schoner": _spec(16.0, 4.2, 1.3, fullness=3.0, stern="counter",
                     masts=[{"x": 0.30, "h": 8.0, "r": 0.09},
                            {"x": 0.62, "h": 10.5, "r": 0.11}]),
    "brig": _spec(20.0, 5.2, 1.6, fullness=3.0, stern="counter", sheer_bow=0.18,
                  sheer_stern=0.14, bulwark=0.22,
                  masts=[{"x": 0.36, "h": 11.0, "r": 0.11, "yards": [0.32, 0.62]},
                         {"x": 0.68, "h": 12.5, "r": 0.12, "yards": [0.30, 0.58]}],
                  gunports=[{"x": 0.62, "w": 0.26, "h": 0.20, "z": 0.62}]),
    "brigantine": _spec(24.0, 5.8, 1.7, fullness=2.8, stern="transom", sheer_bow=0.17,
                         sheer_stern=0.12, bulwark=0.20,
                         masts=[{"x": 0.32, "h": 12.0, "r": 0.11, "yards": [0.30, 0.58]},
                                {"x": 0.66, "h": 14.0, "r": 0.12}]),
    "barque": _spec(30.0, 7.0, 2.1, fullness=3.1, stern="counter", sheer_bow=0.16,
                    sheer_stern=0.12, bulwark=0.20,
                    masts=[{"x": 0.26, "h": 15.0, "r": 0.12, "yards": [0.30, 0.56]},
                           {"x": 0.50, "h": 17.0, "r": 0.13, "yards": [0.30, 0.56]},
                           {"x": 0.76, "h": 15.5, "r": 0.11}]),
    "merchant": _spec(28.0, 6.6, 2.2, fullness=2.9, stern="counter", sheer_bow=0.14,
                      sheer_stern=0.16, bulwark=0.18,
                      masts=[{"x": 0.45, "h": 13.0, "r": 0.12}],
                      cabin={"x": 0.72, "l": 2.4, "w": 3.2, "h": 1.1}),
    "clipper": _spec(34.0, 6.0, 2.0, fullness=3.6, stern="counter", sheer_bow=0.24,
                     sheer_stern=0.16, bulwark=0.16,
                     masts=[{"x": 0.26, "h": 16.0, "r": 0.11, "yards": [0.28, 0.52]},
                            {"x": 0.50, "h": 18.0, "r": 0.12, "yards": [0.28, 0.52]},
                            {"x": 0.74, "h": 16.5, "r": 0.10}]),
    "frigate": _spec(32.0, 6.2, 1.9, fullness=3.0, stern="counter", sheer_bow=0.16,
                     sheer_stern=0.16, bulwark=0.18,
                     masts=[{"x": 0.30, "h": 14.0, "r": 0.11, "yards": [0.30, 0.54]},
                            {"x": 0.62, "h": 15.5, "r": 0.12, "yards": [0.28, 0.52]}],
                     gunports=[{"x": 0.52, "w": 0.26, "h": 0.22, "z": 0.60}]),
    "galleon": _spec(44.0, 9.0, 2.8, fullness=2.7, stern="counter", sheer_bow=0.20,
                     sheer_stern=0.18, bulwark=0.24,
                     masts=[{"x": 0.28, "h": 17.0, "r": 0.14, "yards": [0.28, 0.50]},
                            {"x": 0.52, "h": 20.0, "r": 0.16, "yards": [0.28, 0.50]},
                            {"x": 0.78, "h": 18.0, "r": 0.13}],
                     gunports=[{"x": 0.45, "w": 0.30, "h": 0.26, "z": 0.72},
                               {"x": 0.45, "w": 0.30, "h": 0.26, "z": 0.40}]),
    "manowar": _spec(52.0, 10.5, 3.2, fullness=2.9, stern="counter", sheer_bow=0.14,
                     sheer_stern=0.18, bulwark=0.22,
                     masts=[{"x": 0.26, "h": 20.0, "r": 0.15, "yards": [0.28, 0.50]},
                            {"x": 0.50, "h": 23.0, "r": 0.17, "yards": [0.28, 0.50]},
                            {"x": 0.76, "h": 20.5, "r": 0.14, "yards": [0.26, 0.46]}],
                     gunports=[{"x": 0.45, "w": 0.32, "h": 0.28, "z": 0.75},
                               {"x": 0.45, "w": 0.32, "h": 0.28, "z": 0.42}]),
    "carrack": _spec(38.0, 8.0, 2.6, fullness=2.4, stern="square", sheer_bow=0.16,
                     sheer_stern=0.20, flat_bottom=0.55, bulwark=0.26,
                     masts=[{"x": 0.34, "h": 15.0, "r": 0.14, "yards": [0.30, 0.54]},
                            {"x": 0.70, "h": 13.0, "r": 0.12}]),
    "caravel": _spec(18.0, 4.4, 1.5, fullness=3.1, stern="transom", sheer_bow=0.18,
                     sheer_stern=0.16, bulwark=0.22,
                     masts=[{"x": 0.32, "h": 8.5, "r": 0.09},
                            {"x": 0.64, "h": 9.5, "r": 0.10}]),
    "barge": _spec(15.0, 4.0, 2.4, fullness=2.0, flat_bottom=0.80, stern="square",
                   sheer_bow=0.04, sheer_stern=0.04, deck_frac=0.95, bulwark=0.30),
    "lighter": _spec(11.0, 3.0, 1.8, fullness=2.0, flat_bottom=0.80, stern="square",
                      sheer_bow=0.04, sheer_stern=0.04, deck_frac=0.95, bulwark=0.26),
    "pinnace": _spec(9.0, 2.8, 1.2, fullness=2.8, stern="counter", sheer_bow=0.12,
                     sheer_stern=0.10,
                     masts=[{"x": 0.45, "h": 4.6, "r": 0.07}]),
    "hulk": _spec(36.0, 7.4, 2.6, fullness=2.6, stern="square", sheer_bow=0.28,
                  sheer_stern=0.28, flat_bottom=0.6, bulwark=0.24,
                  masts=[{"x": 0.48, "h": 6.0, "r": 0.14}]),
}


def spec_for(cid):
    s = dict(SHIPS[cid])
    s["name"] = cid
    return s
