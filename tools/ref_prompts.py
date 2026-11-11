"""Prompt builder for Three Horizons reference renders.

Every prompt is assembled from the shared technical conventions of
docs/roadmap/REF-BRIEF.md plus a per-class description, so the whole series
keeps one light, one background and one camera language.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = os.path.join(ROOT, "docs", "roadmap", "model-classes.json")

STYLE = (
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated "
    "vintage palette, slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon."
)

LIGHT = (
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material "
    "boundaries stay readable."
)

BG = "Flat even mid-gray background #B8BEB4, object centered with generous margins, nothing cropped."

NOTEXT = "No lettering, no letters, no digits, no signatures, no watermark."

SCALE = (
    "Next to it a plain measuring ruler with tick marks and a 1.7 m human silhouette for scale, "
    "drawn as simple neutral gray outline shapes without any writing."
)

SHEET = (
    "Technical reference sheet for game modelling and art production, NOT an art poster. "
    "Strict frontal / profile / top projections without perspective distortion."
)


def assembly(desc, sheet=True, scale=True, extra=""):
    parts = []
    if sheet:
        parts.append(SHEET)
    parts.append(desc)
    parts.append(STYLE)
    parts.append(LIGHT)
    parts.append(BG)
    if scale:
        parts.append(SCALE)
    parts.append(NOTEXT)
    if extra:
        parts.append(extra)
    return " ".join(parts)


def detail(desc):
    return assembly(
        "Three Horizons game modular detail element, shown alone and centered: "
        + desc
        + ". Show it in two views: a straight front elevation and a straight side profile, one scale."
    )


def weapon(desc):
    return assembly(
        "Three Horizons game weapon reference for a grounded medieval maritime world, no magic, no runes, "
        "no ornament beyond the description: "
        + desc
        + ". ONE single weapon only, a single object in the frame. Draw it strictly horizontal, in clean "
        "side profile, the entire weapon fully visible and not touching any frame edge. Do NOT draw two "
        "weapons, do NOT draw a pair, do NOT cross them, do NOT overlap them, no X shape, no mirrored "
        "duplicate, no floating extra parts. Render the construction in close readable detail: every "
        "visible fitting, screw, rivet, seam, wrap, pin, ferrule and joint, the grain of the wood, the "
        "wear on the edges, the exact junction between metal and wood and the thickness of the blade or "
        "barrel, so a modeller can rebuild it. The measuring ruler and the human silhouette stand "
        "clearly apart from the weapon, at the far side of the frame, not overlapping it.",
        sheet=False,
    )


def tool(desc):
    return assembly(
        "Three Horizons game profession tool set reference: "
        + desc
        + ". Several tools of the set laid out flat in a neat row on the background, all in one scale, "
        "each tool fully visible and separated.",
        sheet=False,
    )


def item(desc):
    return assembly(
        "Three Horizons game resource item reference: "
        + desc
        + ". The item is shown alone, centered, in three-quarter view, one scale, fully readable.",
        sheet=False,
    )


def tile(desc):
    return assembly(
        "Three Horizons game seamless surface tile reference: "
        + desc
        + ". Show it as a 2x2 grid of identical squares seen strictly from above, flat, with no "
        "perspective, so the seam between the four squares is visible and must not exist.",
        sheet=False,
        scale=False,
        extra="Surface texture only, no object, no props, no frame, no border.",
    )


def ui(desc):
    return assembly(
        "Three Horizons game user interface element, drawn perfectly flat and straight-on with no "
        "perspective and no tilt: " + desc
        + ". Palette strictly: panel background #E8DCC0, secondary #CBB98F, brass frame #B08D3E, "
        "ink #1E1A14, dark wood #3A2A1C, danger #8C2B1B, accent #2E4E7E. Empty placeholder bars "
        "instead of any writing.",
        sheet=False,
        scale=False,
        extra="Element centered on an even neutral page background, same scale as the other UI pieces.",
    )


def weather(desc):
    return assembly(
        "Three Horizons game weather sprite reference: "
        + desc
        + ". The sprite is shown LARGE and centered, flat with no volume and no perspective, a 2D "
        "sprite with soft semi-transparent edges that overlays the scene.",
        sheet=False,
        scale=False,
        extra="Sprite only, no environment, no landscape, no frame.",
    )


def ship(name, size):
    return assembly(
        "Three Horizons game ship hull reference: " + name + ", " + size
        + ". A sheet of three views in a row: three-quarter from slightly above, strict side "
        "profile, strict bow front view. All three views of the same vessel, one scale, so the "
        "waterline and the hull proportions are readable. Medieval sail-and-oar technology with a "
        "subtle ether-driven auxiliary mechanism, plain wooden hull, canvas sails, rope rigging, no "
        "heraldic flags.",
        sheet=False,
        scale=False,
        extra="No text, no labels, no letters, no digits, no watermark.",
    )


CLOTHING = {
    "cloth_t50_плащ_2": assembly(
        "Three Horizons game clothing skin asset, tier 50 formal parade set, item 2 of 7: a "
        "magnificent full-length parade cloak, shown alone on an invisible mannequin in front and "
        "back views, one scale. Deep black-green fine wool with subtle hand-stitched wave filigree "
        "along the hem, high collar, rich dark lining, small aged-brass clasp at the throat, master "
        "tailoring, no jewelry."),
    "cloth_t50_шляпа_с_пером_3": assembly(
        "Three Horizons game clothing skin asset, tier 50 formal parade set, item 3 of 7: a parade "
        "hat with a single feather, shown alone on a neutral display form in front, side and back "
        "views, one scale. Structured black-green felt, narrow dark leather band, one small muted "
        "teal-grey feather at the side, small aged-brass buckle, elegant and restrained."),
    "cloth_t50_перчатки_4": assembly(
        "Three Horizons game clothing skin asset, tier 50 formal parade set, item 4 of 7: a pair of "
        "fine parade gloves, shown alone with palm and back views, one scale. Supple dark brown "
        "leather, reinforced palms, black-green cuffs trimmed with a thin aged-brass edge, precise "
        "master stitching."),
    "cloth_t50_туфли_5": assembly(
        "Three Horizons game clothing skin asset, tier 50 formal parade set, item 5 of 7: a pair of "
        "fine parade shoes, shown alone in side and three-quarter view, one scale. Black-green "
        "polished but worn leather, low heel, small aged-brass buckles, thin dark-green lining "
        "visible at the collar, refined and understated."),
    "cloth_t50_пояс_6": assembly(
        "Three Horizons game clothing skin asset, tier 50 formal parade set, item 6 of 7: an ornate "
        "but restrained parade belt, shown alone laid flat in a straight horizontal band with a "
        "front buckle view. Dark brown tooled leather with black-green edging and an aged-brass "
        "buckle, punched holes, master stitching, no hanging accessory."),
    "cloth_t50_цепочка_7": assembly(
        "Three Horizons game clothing skin asset, tier 50 formal parade set, item 7 of 7: a fine "
        "ceremonial chain necklace, shown alone laid in a relaxed closed loop with a clasp detail "
        "view. Aged brass links with small dark-green enamel accents, hand-forged, restrained and "
        "elegant, no pendant, no gemstones."),
}


DETAILS = {
    "det_roof_gable": "a two-slope gable roof module with clay tiles and exposed rafter ends",
    "det_roof_hip": "a four-slope hipped roof module with clay tiles and a ridge cap",
    "det_roof_flat": "a flat roof module with a tar-and-gravel surface and a low stone edge",
    "det_roof_tower": "a conical tower roof module with slate tiles and a small finial",
    "det_roof_sawtooth": "a saw-tooth industrial roof module with repeated glazed north faces",
    "det_roof_mansard": "a mansard roof module with steep lower and shallow upper slopes",
    "det_ridge": "a roof ridge cap module, a capped tile ridge running horizontally",
    "det_eave": "an eave module, the overhanging roof edge with rafter tails",
    "det_eaves_board": "a fascia board module closing the eave, painted timber",
    "det_gutter": "a half-round wooden gutter module with a simple bracket",
    "det_downpipe": "a timber downpipe module with a hopper head and brackets",
    "det_chimney": "a masonry chimney module with a simple cap and a clay pot",
    "det_beam_horizontal": "a horizontal squared timber beam with chamfered ends and peg holes",
    "det_beam_vertical": "a vertical squared timber post with a chamfered top and peg holes",
    "det_brace_diagonal": "a diagonal timber brace, mortise-and-tenon joints visible",
    "det_timber_frame": "a half-timbered wall panel with diagonal braces and plaster infill",
    "det_foundation": "a rough rubble foundation course under a wall",
    "det_plinth_stone": "a dressed stone plinth course with chisel marks",
    "det_stairs": "an exterior stone stair flight with worn treads",
    "det_stairs_rail": "a timber stair handrail with turned newel post and balusters",
    "det_balcony": "a small cantilevered timber balcony platform on brackets",
    "det_balcony_rail": "a timber balcony balustrade with turned spindles",
    "det_window_frame": "a stone-framed window opening with a timber inner frame",
    "det_window_mullion": "a timber window mullion with a glazing bar",
    "det_window_sill": "a sloped stone window sill with a drip groove",
    "det_window_shutters": "a pair of wooden window shutters with iron hinges, one open one closed",
    "det_window_grate": "an iron window grate with vertical bars",
    "det_door_frame": "a stone doorway surround with a timber inner frame",
    "det_door_leaf": "a heavy timber door leaf with vertical planks and iron straps",
    "det_door_hinges": "a wrought-iron door hinge strap with pintle",
    "det_door_ring": "an iron door ring pull on a decorative backplate",
    "det_arch_stone": "a single stone arch of a doorway or window",
    "det_bracket": "a carved stone corbel bracket supporting a balcony",
    "det_corbel": "a rough stone corbel block projecting from a wall",
    "det_corner_stone": "a dressed quoin stone for a building corner",
    "det_sill_band": "a horizontal band of stone around a plinth",
    "det_wainscot": "a timber wainscot panelling section with vertical boards and a rail",
    "det_lintel": "a timber lintel beam over an opening with peg ends",
    "det_gable_board": "a horizontal gable board closing the top of a gable wall",
    "det_bargeboard": "a barge board following the slope of a roof edge",
    "det_gutter_join": "a joint piece joining two gutter runs, with a bracket",
    "det_wall_cap": "a coping cap along the top of a wall",
    "det_merlon": "a single crenellation merlon block of a rampart",
    "det_battlement": "a short run of crenellated rampart wall with merlons and crenels",
    "det_banner": "a plain hanging cloth banner on a timber pole, no emblem",
    "det_lantern": "a brass lantern hanging from a wall bracket",
    "det_wheel": "a wooden ship's steering wheel with spokes and a hub",
    "det_capstan": "a wooden ship's capstan with bar holes and a rope wrap",
    "det_cleat": "a cast iron mooring cleat on a base plate",
    "det_bollard": "a heavy timber mooring bollard with a rope coil",
    "det_ladder": "a wooden rope ladder with side rails and wooden steps",
    "det_gangway": "a wooden ship's gangway with side rails and a hinge",
    "det_crane_arm": "a timber jib crane arm with a pulley block at the tip",
    "det_crane_hook": "an iron crane hook on a short chain",
    "det_rigging_rope": "a coil of hemp rigging rope with a whipped end",
    "det_block_pulley": "a wooden pulley block with an iron sheave and an eye",
    "det_hatch": "a small cargo hatch with a timber lid and iron hinges",
    "det_grating": "a timber deck grating panel",
    "det_anchor_stock": "an anchor stock with a wooden crossbeam and iron ring",
    "det_funnel": "a ship's funnel or exhaust trunk with a cowl",
    "det_vent": "a mushroom-shaped ventilation cowl on a deck",
    "det_scupper": "a scupper hole with a timber lining in a ship's side",
    "det_rowlock": "an iron rowlock oarlock pin for a rowing bench",
    "det_oar": "a single wooden oar with a worn blade and a rope loop",
}


ITEMS = {
    "wood": "a bundle of cut logs bound with rope",
    "planks": "a neat stack of sawn timber planks",
    "ore": "a woven basket full of rough dark ore stones",
    "metal": "a short stack of dull grey metal ingots",
    "parts": "an open wooden crate holding small brass and iron mechanical parts",
    "fiber": "a hank of raw fiber twine",
    "cloth": "a folded bolt of woven cloth",
    "clothes": "a folded stack of plain garments",
    "ether_raw": "a cluster of raw ether crystals, cold pale blue #3FA7FF, translucent and faceted",
    "fuel": "a sealed wooden barrel of ether fuel with a brass valve, pale blue liquid sheen",
    "grain": "a stitched sack of sky grain, warm ochre #D8A93B kernels visible at the open mouth",
    "flour": "a stitched sack of flour, pale cream, soft powder visible at the open mouth",
    "bread": "a round rustic loaf of dark bread on a plain board",
    "aquacrystal": "a single aquacrystal crystal, icy translucent blue #7FD4FF, faceted, held in a plain clamp",
}


TOOLS = {
    "tool_engineer": "engineer's tools, calipers, a folding rule, a small hand drill and a rolled drawing",
    "tool_smith": "blacksmith's tools, a small hammer, tongs, a chisel set and a swage block",
    "tool_carpenter": "carpenter's tools, a hand plane, a chisel, a wooden mallet and a marking gauge",
    "tool_navigator": "navigation instruments, a magnetic compass, a brass dividers, a sextant and a rolled chart",
    "tool_seaman": "seaman's tools, a belaying pin, a serving mallet, a fid and a coil of small rope",
    "tool_trader": "trade scales and weights, a small balance scale and a set of cast iron weights",
    "tool_farmer": "farm tools, a sickle, a hoe, a seed dibber and a scythe whetstone",
    "tool_hunter": "hunting gear, a hunting knife, a snare cord, a calls pouch and a spare arrow bundle",
    "tool_shooter": "gunnery accessories, a powder flask, a patch box, a wadding rod and a cleaning brush",
    "tool_fencer": "fencing accessories, a fencing mask, a padded jacket, a bell guard and a foil glove",
    "tool_repair": "repair tools, a hammer, pliers, a hand drill, a sewing kit of sail needle and waxed thread",
    "tool_manager": "office supplies, a quill stand, an ink pot, a ledger, a sealing wax stick and a letter rack",
    "tool_mason": "mason's tools, a mason's hammer, a plumb bob, a chalk line and a trowel",
    "tool_cooper": "cooper's tools, a draw knife, a hoop driver, an adze and a planing stock",
    "tool_leather": "leatherworking tools, a round knife, an awl, a stitching shuttle and a wooden mallet",
    "tool_glass": "glassmaking tools, a blowing pipe, a glass cutter, a wooden pontil and a pair of jacks",
}


TILES = {
    "tile_stone_wall": "a weathered cut stone wall surface, cool grey mortar joints",
    "tile_plaster": "a smooth lime plaster wall surface, warm off-white with faint patches",
    "tile_wood_floor": "worn oak plank flooring, visible grain and nail heads",
    "tile_roof_slate": "overlapping grey slate roof tiles",
    "tile_roof_thatch": "golden straw thatch roofing, overlapping bundles",
    "tile_roof_tile": "red-brown clay roof tiles in overlapping rows",
    "tile_dirt": "dry packed earth with small pebbles",
    "tile_grass_patch": "short uneven meadow grass with a few small flowers",
    "tile_gravel": "grey crushed gravel ballast",
    "tile_sand": "pale warm sand with faint ripples",
    "tile_mud": "wet dark mud with shallow puddles and footprints",
    "tile_snow": "fresh snow with soft wind-shaped drifts",
    "tile_cliff": "cracked grey cliff rock with mineral veins",
    "tile_cobble": "rounded grey cobblestone paving with sandy joints",
    "tile_crate_stack": "stacked wooden shipping crates seen from above, tight fit with no gaps",
    "tile_net": "coiled fishing net with cork floats, seen from above",
    "tile_rope": "coiled hemp mooring ropes laid flat in overlapping circles",
    "tile_rack": "a timber storage rack shelf surface with crates and sacks packed tight",
}


UI = {
    "ui_icon": "a small square icon frame with an abstract anchor-and-rope glyph inside",
    "ui_badge": "a small rounded counter badge with an empty value plate attached to an icon frame",
    "ui_tab": "a horizontal tab strip with three tabs, the middle one raised",
    "ui_slider": "a horizontal slider track with a brass handle at the middle",
    "ui_toggle": "a switch toggle in two states, off and on, side by side",
    "ui_checkbox": "a square checkbox with a check mark, and an empty one beside it",
    "ui_radio": "a round radio button with a filled center, and an empty one beside it",
    "ui_tooltip": "a small tooltip bubble with a pointer tail and one empty line",
    "ui_progress": "a horizontal progress bar filled about two thirds",
    "ui_meter": "a horizontal scale gauge with tick marks and a needle",
    "ui_compass": "a round compass rose with a needle and a cardinal ring of plain ticks",
    "ui_minimap": "a square minimap panel with abstract coast shapes and a position marker",
    "ui_dialog": "a dialog window with a title bar, an empty text area and two buttons",
    "ui_toolbar": "a horizontal toolbar with six square slot frames",
    "ui_hotbar": "a row of eight small square quick-access slots with one filled",
    "ui_craft": "a crafting panel with an input slot, an output slot and a list of empty rows",
    "ui_ship_hud": "a ship HUD strip with a sail gauge, a speed dial and three status bars",
    "ui_trade_panel": "a trade panel with two item columns, price rows and one button",
    "ui_currency": "a small currency plate with a coin icon and an empty value box",
    "ui_timer": "a timer plate with a circular dial and a small pointer",
    "ui_tooltip_icon": "a small round icon badge for a tooltip corner, with an abstract glyph",
}


WEAPONS = {
    "cutlass": "a curved naval boarding cutlass, short and broad, with a knuckle guard",
    "rapier": "a slender thrusting rapier with a swept hilt and a small cup guard",
    "sword": "a plain medieval arming sword with a straight double-edged blade and a cross guard",
    "longsword": "a long arming sword, fuller down the blade, straight cross guard",
    "greatsword": "a very long two-handed greatsword with a long straight blade",
    "sabre": "a light curved cavalry sabre with a single edge",
    "broadsword": "a wide blunt-edged broadsword with a shallow fuller and a wide cross guard",
    "falchion": "a wide single-edged falchion with a strongly curved chopping blade",
    "estoc": "a narrow thrusting estoc with a triangular blade and a small knuckle guard",
    "dagger": "a short broad dagger with a simple cross guard and a pommel",
    "dirk": "a narrow Scottish dirk with a straight double-edged blade",
    "mainchou": "a heavy plain mainsail cutlass with a thick curved blade and a basket hilt",
    "club": "a short wooden club, a heavy rounded head on a thick shaft",
    "mace": "a flanged steel mace with a plain shaft and a round head",
    "warhammer": "a war hammer with a long shaft, a blunt hammer head and a spike",
    "spear": "a long infantry spear with a leaf-shaped socketed blade",
    "lance": "a long cavalry lance with a small spearhead and a plain shaft",
    "halberd": "a halberd with an axe blade, a spike and a hook on a long shaft",
    "pike": "a very long pike with a narrow spearhead on a thick shaft",
    "trident": "a three-pronged marine trident with a long shaft",
    "glaive": "a single-edged glaive with a long slightly curved blade",
    "axe": "a single-bit felling axe with a wooden haft",
    "battleaxe": "a broad battle axe with a bearded steel head and a riveted haft",
    "beardedaxe": "a narrow bearded axe with a deep crescent blade",
    "handaxe": "a small one-handed hand axe with a short haft",
    "waraxe": "a heavy axe with a broad polished blade and a short haft",
    "poleaxe": "a long-shafted pole axe with a spike, axe blade and rear fluke",
    "sling": "a simple leather sling with a pouch and a cord",
    "atlatl": "an atlatl spear-thrower, a wooden dart with a finger loop and a throwing board",
    "javelin": "a throwing javelin with a narrow leaf-shaped head and a rope binding",
    "dart": "a small throwing dart with a slim iron head",
    "flintlock": "a flintlock pistol with a curved wooden grip, brass fittings and a small flintlock mechanism",
    "miquelet": "a miquelet pistol with a long narrow barrel, a box lock and a curved stock",
    "snaphance": "a snaphance pistol with a visible cock holding the flint and a dog-eared lock",
    "wheellock": "a wheellock pistol with a visible clockwork wheel mechanism and a heavy stock",
    "blunderbuss": "a blunderbuss with a very short wide flared barrel and a heavy stock",
    "musket": "a long musket with a smooth barrel, a matchlock-style brown stock and a bayonet lug",
    "caliver": "a short caliver musket with a heavy barrel and a plain stock",
    "arquebus": "a heavy arquebus with a very long barrel and a solid butt",
    "pistol": "a plain smoothbore duelling pistol with a simple brown stock",
    "carbine": "a short carbine with a compact barrel and a curved stock",
    "rifle": "a rifled long gun with a long barrel, a shaped stock and a simple percussion-style lock",
    "axe_marine": "a boarding axe with a heavy wedge head, a spike on the back and a short haft",
    "boardingpike": "a boarding pike with a thick shaft, a broad leaf blade and a metal collar",
    "cutlass_sail": "a sailor's heavy cutlass with a broad slightly curved blade and a plain guard",
}

# Rendering order chosen by the user (2026-11-11): the axe and pole families are
# done, the bow family is dropped entirely, and the remaining weapons are shot in
# this order - firearms first, then the ship-boarding set, then thrown weapons.
WEAPON_ORDER = [
    "flintlock",
    "miquelet",
    "snaphance",
    "wheellock",
    "blunderbuss",
    "musket",
    "caliver",
    "arquebus",
    "pistol",
    "carbine",
    "rifle",
    "axe_marine",
    "boardingpike",
    "cutlass_sail",
    "atlatl",
    "javelin",
    "dart",
]


WEATHER = {
    "wx_fog_bank": "a low horizontal bank of fog, a soft elongated sheet of pale vapour",
    "wx_cumulus_large": "a large single cumulus cloud mass with a flat base and rounded top",
    "wx_cumulus_small": "a small compact cumulus cloud puff",
    "wx_stratus": "a wide flat layered stratus cloud sheet with soft horizontal banding",
    "wx_cirrus": "wispy streaked cirrus cloud filaments",
    "wx_nimbus": "a heavy rain-bearing nimbus cloud mass with a dark flat base",
    "wx_mist": "a thin low mist hugging the surface, a soft flat translucent layer",
    "wx_vortex": "a swirling vortex of cloud, a spiral funnel of vapour",
    "wx_lightning": "a single forked lightning bolt, bright pale blue-white with a soft glow",
    "wx_rain_cloud": "a dark rain cloud with visible falling rain streaks beneath it",
}


SHIPS = {
    "skiff": ("a small open skiff", "4 x 1.5 m, hull height 0.8 m", "a plain flat-floored boat with three rowing thwarts, no mast, a simple oar and a stern oarlock, plain dark planks"),
    "trawler": ("a small coastal trawler", "7 x 2.5 m, hull height 1.0 m", "a single small mast with a short gaff sail, an open aft working deck with a net drum and a low fish hatch"),
    "sloop": ("a single-masted sloop", "10 x 3.5 m, hull height 1.2 m", "one mast with a mainsail and a jib, a short bowsprit, a modest foredeck and an open stern"),
    "cutter": ("a fast small cutter", "14 x 4.5 m, hull height 1.4 m", "one raked mast with a square topsail, a long bowsprit, a narrow sharp hull and a small quarterdeck"),
    "smack": ("a sturdy coastal smack", "12 x 3.2 m, hull height 1.1 m", "one short mast with a gaff mainsail and a small jib, a raised bulwark and a small open hold"),
    "schooner": ("a two-masted schooner", "16 x 4.2 m, hull height 1.3 m", "two raked masts with fore-and-aft gaff sails, a long bowsprit and a low flush deck"),
    "brig": ("a two-masted square-rigged brig", "20 x 5.2 m, hull height 1.6 m", "two masts with square sails on yards, a bowsprit, a high forecastle and a square stern"),
    "brigantine": ("a brigantine", "24 x 5.8 m, hull height 1.7 m", "a square rig on the fore mast and a gaff rig on the main mast, a bowsprit, a raised quarterdeck"),
    "barque": ("a three-masted barque", "30 x 7.0 m, hull height 2.1 m", "square sails on fore and main, a gaff sail on the mizzen, a long bowsprit, a full-rigged hull"),
    "merchant": ("a broad-beamed cargo merchantman", "28 x 6.6 m, hull height 2.2 m", "two masts with square sails, a wide flat cargo deck with two hatch coamings and a heavy sheer, built for bulk cargo"),
    "clipper": ("a fast clipper", "34 x 6.0 m, hull height 2.0 m", "three masts with extensive square and gaff sail plan, a long fine bow and a narrow deep hull with a raked sternpost"),
    "frigate": ("a warship frigate", "32 x 6.2 m, hull height 1.9 m", "three masts with square sails, a long gun deck with a row of gun ports and a quarter gallery at the stern"),
    "galleon": ("a heavy galleon", "44 x 9.0 m, hull height 2.8 m", "three masts with square sails, a tall poop deck, a high stern castle, two gun decks with rows of gun ports and heavy carved work"),
    "manowar": ("a first-rate line-of-battle ship", "52 x 10.5 m, hull height 3.2 m", "three masts with full square rig, three gun decks with dense rows of gun ports, a tall stern castle and a strongly curved hull"),
    "carrack": ("a three-masted carrack", "38 x 8.0 m, hull height 2.6 m", "three masts with a square rig, a high forecastle and a very high stern castle, a broad rounded hull"),
    "caravel": ("a nimble caravel", "18 x 4.4 m, hull height 1.5 m", "two or three lateen masts with triangular sails, a high poop, a low narrow hull with a pronounced sheer"),
    "barge": ("a flat-bottomed cargo barge", "15 x 4.0 m, hull height 2.4 m", "no rig at all, a wide flat cargo deck with side rails, a square stern and a blunt bow"),
    "lighter": ("a flat lighter barge", "11 x 3.0 m, hull height 1.8 m", "a flat-floored open lighter with high solid sides, a small aft cabin and no rig"),
    "pinnace": ("a small pinnace", "9 x 2.8 m, hull height 1.2 m", "one small mast with a square sail, a small raised stern cabin, an open waist and a short bowsprit"),
    "hulk": ("a bulky hulk", "36 x 7.4 m, hull height 2.6 m", "a heavy blunt-bowed hull with minimal rig, one short mast with a plain square sail, a tall rounded stern and a weathered working deck"),
}


def build_all():
    out = {}
    for key, val in CLOTHING.items():
        out[key] = val
    for key, val in DETAILS.items():
        out[key] = detail(val)
    for key, val in ITEMS.items():
        out[key] = item(val)
    for key, val in TOOLS.items():
        out[key] = tool(val)
    for key, val in TILES.items():
        out[key] = tile(val)
    for key, val in UI.items():
        out[key] = ui(val)
    for key, val in WEAPONS.items():
        out[key] = weapon(val)
    for key, val in WEATHER.items():
        out[key] = weather(val)
    for key, (name, size, desc) in SHIPS.items():
        out[key] = ship(name, size + ", " + desc)
    return out


def main():
    data = json.load(open(CLASSES, encoding="utf-8"))
    prompts = build_all()
    wanted = sys.argv[1:] if len(sys.argv) > 1 else []
    if wanted:
        for key in wanted:
            cid = next((c["id"] for c in data["classes"] if c["id"] == key), None)
            if cid is None:
                print("!! unknown id %s" % key)
                continue
            print("=== %s ===" % cid)
            print(prompts[cid])
    else:
        for c in data["classes"]:
            if c["id"] in prompts:
                print("=== %s ===" % c["id"])
                print(prompts[c["id"]])


if __name__ == "__main__":
    main()
