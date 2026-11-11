"""Prompt builder for the Three Horizons reference images.

One template per model-class group; the subject phrase comes from
`subjects.json` (id -> subject / notes).
"""

COMMON = (
    "Three Horizons game reference sheet for a grounded medieval maritime world: no magic, no runes, "
    "no ornament beyond the description. This is a TECHNICAL SAMPLE for game modelling and art production, "
    "NOT an art poster: I need readable form and materials, not mood. "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material boundaries stay readable. "
    "Flat even mid-gray background #B8BEB4, object centered with generous margins, nothing cropped, nothing touching the frame edge. "
    "No lettering, no letters, no digits, no signatures, no watermark."
)

SCALE = (
    "Next to it a plain measuring ruler with tick marks and a 1.7 m human silhouette for scale, "
    "drawn as simple neutral gray outline shapes without any writing, standing clearly apart from the object, "
    "at the far side of the frame, not overlapping it."
)

WEAPON = (
    "Three Horizons game weapon reference for a grounded medieval maritime world, no magic, no runes, "
    "no ornament beyond the description: {subject}. "
    "ONE single weapon only, a single object in the frame. Draw it strictly horizontal, in clean side profile, "
    "the entire weapon fully visible and not touching any frame edge. "
    "Do NOT draw two weapons, do NOT draw a pair, do NOT cross them, do NOT overlap them, no X shape, "
    "no mirrored duplicate, no floating extra parts. "
    "Render the construction in close readable detail: every visible fitting, screw, rivet, seam, wrap, pin, "
    "ferrule and joint, the grain of the wood, the wear on the edges, the exact junction between metal and wood "
    "and the thickness of the blade or barrel, so a modeller can rebuild it. "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material boundaries stay readable. "
    "Flat even mid-gray background #B8BEB4, object centered with generous margins, nothing cropped. "
    "The measuring ruler and the human silhouette stand clearly apart from the weapon, at the far side of the frame, "
    "not overlapping it. No lettering, no letters, no digits, no signatures, no watermark."
)

DETAIL = (
    "Three Horizons game modular building and ship detail reference: {subject}. "
    "ONE single part only, one object in the frame, shown straight-on and isolated so its construction is fully readable. "
    "Do NOT show the assembled building or ship, do NOT show the part twice, do NOT repeat it, no mirrored duplicate, "
    "no floating extra pieces. Render the construction in close readable detail: every visible joint, seam, tenon, "
    "mortise, nail, rivet, peg, bracket, groove, bevel, dowel and edge, the grain of the wood, the tool marks, "
    "the wear on the edges, and the exact junction between the materials, so a modeller can rebuild the module. "
    "{scale} "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material boundaries stay readable. "
    "Flat even mid-gray background #B8BEB4, part centered with generous margins, nothing cropped. "
    "No lettering, no letters, no digits, no signatures, no watermark."
)

ITEM = (
    "Three Horizons game resource item reference for a grounded medieval maritime economy: {subject}. "
    "ONE single item pile only, one grouping in the frame, centered and completely visible, nothing cropped. "
    "Do NOT spread the material into a flat pile of many separate pieces, do NOT duplicate the pile, "
    "no mirrored duplicate, no extra objects. "
    "Render it in close readable detail: every visible plank, log end, grain line, metal facet, weave, fold, "
    "seam, label-free surface, chip and crack, the wear on the edges, so a modeller can rebuild the inventory icon. "
    "{scale} "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material boundaries stay readable. "
    "Flat even mid-gray background #B8BEB4, item centered with generous margins, nothing cropped. "
    "No lettering, no letters, no digits, no signatures, no watermark."
)

TOOLSET = (
    "Three Horizons game profession tool-set reference: {subject}. "
    "A small group of tools belonging to ONE trade, laid out flat next to each other on the ground plane, "
    "all of them fully visible and NOT overlapping each other, each tool readable on its own. "
    "Do NOT add unrelated tools, do NOT duplicate a tool, no mirrored duplicate, no floating extra parts. "
    "Render the construction in close readable detail: every visible blade edge, haft, grip, ferrule, rivet, "
    "seam, tooth, the grain of the wood, the wear on the edges and the junction between metal and wood, "
    "so a modeller can rebuild each tool. "
    "{scale} "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material boundaries stay readable. "
    "Flat even mid-gray background #B8BEB4, tools centered with generous margins, nothing cropped. "
    "No lettering, no letters, no digits, no signatures, no watermark."
)

SHIP = (
    "Three Horizons game ship hull reference for a grounded medieval maritime world: {subject}. "
    "ONE single ship hull only, shown in a clean full broadside view, strictly horizontal, the whole hull "
    "from bow to stern fully visible and not touching any frame edge, waterline level, no perspective distortion. "
    "Do NOT draw the ship twice, do NOT draw a mirror duplicate, do NOT overlap two hulls, no X shape. "
    "Show the hull itself: the planking courses and seams, the stem and stern posts, the sheer line, the gun ports "
    "or oar ports, the rails, the wale, the rudder and the mooring fittings, plus simple bare masts and spars "
    "without rigging if the class needs them. Render the construction in close readable detail so a modeller "
    "can rebuild the hull. {notes} "
    "{scale} "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material boundaries stay readable. "
    "Flat even mid-gray background #B8BEB4, hull centered with generous margins, nothing cropped. "
    "No lettering, no letters, no digits, no flags, no signatures, no watermark."
)

TILE = (
    "Three Horizons game seamless surface texture tile: {subject}. "
    "A flat square texture sheet seen STRICTLY FROM ABOVE, no perspective, no 3D view, filling the frame as one "
    "continuous surface so that the tile edges match and it repeats seamlessly in every direction. "
    "Even diffuse light, no dramatic shadows, no vignette, no object in the centre. "
    "Render the surface material in close readable detail: the grain, the pattern, the wear, the chips, the mortar "
    "or the weave, so a modeller can rebuild and tile the surface. "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon. "
    "No lettering, no letters, no digits, no signatures, no watermark."
)

UI = (
    "Three Horizons game UI element reference: {subject}. "
    "A flat 2D interface element shown STRAIGHT ON, no perspective, no tilt, no mockup scene, no device frame, "
    "no background scene behind it, isolated on a flat even mid-gray background #B8BEB4. "
    "Render it as a clean, readable, game-ready widget: crisp simple shapes, thin even outlines, "
    "muted desaturated parchment-and-ink palette with a single accent, no gradients that hide the silhouette. "
    "The element contains NO text, NO letters, NO numbers, no icons that are not described, no signatures, no watermark. "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots. "
    "Element centered with generous margins, nothing cropped."
)

WEATHER = (
    "Three Horizons game weather and sky element: {subject}. "
    "A flat, wide sheet element seen strictly frontally, with a soft dissolving edge like a brush stroke or haze, "
    "so the alpha silhouette of the whole shape is visible. It is NOT a volumetric 3D cloud, NOT fluffy cotton wool, "
    "no hard 3D boundaries, no cast shadow, no ground, no environment. "
    "Even diffuse light, muted desaturated vintage palette, slight old-film grain, "
    "styled realism + medieval maritime + vintage exploration, no neon, no cartoon. "
    "Flat even mid-gray background #B8BEB4 around the shape, shape centered with generous margins, nothing cropped. "
    "No lettering, no letters, no digits, no signatures, no watermark."
)

TEMPLATES = {
    "weapons": WEAPON,
    "details": DETAIL,
    "items": ITEM,
    "tools": TOOLSET,
    "ships": SHIP,
    "tiles": TILE,
    "ui": UI,
    "weather": WEATHER,
}

ASPECT = {
    "weapons": "1:1",
    "details": "1:1",
    "items": "1:1",
    "tools": "1:1",
    "ships": "21:9",
    "tiles": "1:1",
    "ui": "1:1",
    "weather": "16:9",
}


SHIP_STYLE = (
    "Three Horizons game ship reference for a grounded medieval maritime world, no magic, no runes, "
    "no ornament beyond the description. This is a TECHNICAL SAMPLE for game modelling and art production, "
    "NOT an art poster: I need readable form and materials, not mood. "
    "Style: stylized realism + medieval maritime + vintage exploration, muted desaturated vintage palette, "
    "slight old-film grain. No fantasy, no steampunk, no cartoon styling, no neon, no modern fittings. "
    "Even diffuse light, no dramatic shadows, no rim light, no specular hotspots, so material boundaries stay readable. "
    "Painted and weathered surfaces in muted desaturated colors, like a real working vessel: NOT a white plaster, "
    "clay or unpainted studio model. "
    "Flat even mid-gray background #B8BEB4, the vessel centered with generous margins, nothing cropped, "
    "nothing touching the frame edge. No lettering, no letters, no digits, no emblems, no signatures, no watermark."
)

# Every ship class gets its own prompt: a different framing, a different set of
# construction details and a different scale device, so the 20 references read as
# a hull bible instead of one template with a swapped name.
SHIP_PROMPTS = {
    "skiff": (
        "A tiny open rowing skiff seen from high above and slightly in front, so the whole interior is visible: "
        "the flat floor with its ribs, three thwarts, a pointed stem and a square transom, weathered painted planking "
        "in muted grey-green with a tarred bottom and visible seams and nail heads, a single pair of oars shipped along "
        "the gunwale, and a coil of rope at the bow. "
        "No mast, no sail, no rigging. The boat is only a little longer than the standing figure on the quay beside it, "
        "which gives the scale; a plain ruler with tick marks lies flat on the ground next to that figure. "
        "One vessel only, no second boat, no reflection, no water surface."
    ),
    "trawler": (
        "A small decked fishing trawler in a clean broadside elevation, hull and deck gear both readable: "
        "a blunt raked stem, a low sheer, a single working deck with a raised hatch coaming amidships, a hand winch "
        "on a timber drum, a net drum with rope coiled on it, an iron anchor stowed on the fore deck and a short rail "
        "of vertical stanchions. The hull is tarred black with a pale sheer stripe and salt-worn planking at the waterline. "
        "A 1.7 m human silhouette stands on the deck by the winch, and a plain ruler with tick marks lies on the ground "
        "under the hull. One vessel only."
    ),
    "sloop": (
        "A small single-masted sloop in a bow three-quarter view from slightly above, showing the curve of the raked "
        "stem, the rounded transom and the low cabin trunk with its sliding hatch and a single port on each side. "
        "The bare mast sits in a visible tabernacle with partners, a simple gaff and boom are shipped along the "
        "boom crutch, and a coil of halyard hangs on the pin rail. Inside the open cockpit a tiller and a small "
        "compass binnacle are visible. One vessel only, no water, no reflection, no second boat. "
        "A 1.7 m human silhouette stands at the stern rail for scale, with a plain ruler with tick marks laid on the ground beside her."
    ),
    "cutter": (
        "A narrow fast cutter in a strict side profile, drawn long and low so the fine entry of the bow and the long "
        "overhang aft are the whole subject of the picture: a sharply raked stem, a very clean straight sheer, a "
        "plumb stern with a small counter, a bowsprit carried on a bowsprit shroud, and a single bare mast with a "
        "standing rigging of shrouds and ratlines. The planking is flush and the strakes run unbroken from stem to stern. "
        "One vessel only. A 1.7 m human silhouette stands on the foredeck and a plain ruler with tick marks "
        "runs along the ground below the keel line."
    ),
    "smack": (
        "A sturdy bluff-bowed smack in a low broadside view that shows both the working deck and the raised quarterdeck: "
        "a fat rounded bow with a short bowsprit, a low forecastle, a quarterdeck raised a step above the waist, "
        "a wide transom with a simple taffrail, carvel planking with a painted band along the sheer, a single mast "
        "stepped well forward, and a working deck with a capstan and coiled hawser. "
        "One vessel only. A 1.7 m human silhouette stands on the quarterdeck against the transom for scale, "
        "and a plain ruler with tick marks lies flat on the ground under the hull."
    ),
    "schoner": (
        "A two-masted schoner in a clean side elevation whose subject is the rig ratio: the short foremast stepped "
        "forward, the tall mainmast stepped abaft the midships, both bare with yards and a gaff, plus the fore-and-aft "
        "standing rigging and the boom lying along the deck. The hull is narrow with a long low deck, a raked stem, "
        "a modest sheer and a narrow plumb stern, with a low hatch and a small wheelhouse amidships. "
        "One vessel only, no sails set, no rigging lines crossing the frame. "
        "A 1.7 m human silhouette stands on the foredeck, and a plain ruler with tick marks lies under the keel."
    ),
    "brig": (
        "A square-rigged brig in a full broadside elevation showing the hull and the whole sail plan at once: two tall "
        "masts with two square yards each, standing rigging of shrouds and ratlines, the bowsprit with its spritsail "
        "yard, the hull with a pronounced sheer, a rounded counter stern and a single row of gun ports along the "
        "quarterdeck, carvel planking with a painted wale, a bowsprit anchor and a quarterdeck rail. "
        "One vessel only. A 1.7 m human silhouette stands on the quarterdeck near the mainmast for scale, "
        "and a plain ruler with tick marks runs along the ground under the hull."
    ),
    "brigantine": (
        "A brigantine in a bow three-quarter view from the port side and slightly above, showing the fuller bow and "
        "the long rising sheer: a broad rounded forefoot, a straight stem, a square tuck transom, the square rig on the "
        "foremast with two yards and the long gaff and boom of the mainmast, a wide waist with a large hatch and a "
        "capstan abaft the foremast, and a raised quarterdeck with a ladder to it. "
        "One vessel only, no sails set. A 1.7 m human silhouette stands on the bowsprit netting for scale, "
        "with a plain ruler with tick marks laid on the ground beside the hull."
    ),
    "barque": (
        "A large three-masted barque in a full broadside elevation, the picture organised around its rig and its long "
        "run: square yards on the fore and main masts, a fore-and-aft gaff on the mizzen, a tall mainmast with a "
        "fighting top, the hull with a deep keel, a long fine run to a rounded counter, a high quarterdeck with "
        "a row of small scuttles and a plain taffrail, and a boat on the davits amidships. "
        "One vessel only, no sails set. A 1.7 m human silhouette stands on the quarterdeck for scale, "
        "and a plain ruler with tick marks lies along the ground under the whole length of the keel."
    ),
    "merchant": (
        "A broad-beamed merchant ship in a broadside elevation photographed as a working cargo vessel: the hull with a "
        "high rounded stern castle of two decks with small windows, a low waist with two large square cargo hatches, "
        "a crow's nest on the mainmast, a single heavy mast with a gaff, the cargo derrick rigged over the main hatch, "
        "a ladder to the quarterdeck, a tarred hull with a pale band, and an anchor stowed on the fore deck. "
        "One vessel only, no sails set. A 1.7 m human silhouette stands on the quarterdeck near the ladder for scale, "
        "and a plain ruler with tick marks lies on the ground under the hull."
    ),
    "clipper": (
        "A clipper in a strict profile built around its waterlines: the fine near-vertical entry of the stem, the "
        "long run, the very sharp overhanging counter, the deep keel and the three tall masts with their yards, "
        "the hull showing a working topside, a narrow waist with a single hatch, the carved head rails and a "
        "figurehead-less bow without ornament, the deck equipment of a capstan and a wheel amidships. "
        "One vessel only. A 1.7 m human silhouette stands on the poop deck for scale, "
        "and a plain ruler with tick marks is laid on the ground parallel to the keel."
    ),
    "frigate": (
        "A war frigate in a three-quarter view from the port bow, showing the battery and the stern at once: the "
        "square bow with its carved head rails, a single complete gun deck with evenly spaced gun ports and lids "
        "hinged open, a channel with a deadeye and its chain, a plain quarterdeck with a wheel and a whipstaff, "
        "a long square stern with a plain gallery of small square windows, and the standing rigging of the fore shrouds. "
        "One vessel only. A 1.7 m human silhouette stands on the foredeck for scale, "
        "and a plain ruler with tick marks lies on the ground in front of the bow."
    ),
    "galleon": (
        "A galleon in a full broadside elevation with the whole high-sided form readable: a strongly curved stem with "
        "a long projecting beakhead and its head rails, a high rounded stern castle of three decks with square windows, "
        "two complete gun decks of gun ports, a rounded bilge in the hull, a gilded but plain taffrail, a mainmast and "
        "mizzen stepped through the deck with a bowsprit, a waist with an open hatch and a capstan, and a deck full of "
        "running rigging. One vessel only, no sails set. A 1.7 m human silhouette stands on the quarterdeck for scale, "
        "and a plain ruler with tick marks runs along the ground under the hull."
    ),
    "manowar": (
        "A line-of-battle ship in a complete side elevation, the largest hull of the series: a straight vertical stem "
        "with a straight stem knee, a very high stern with a tiered gallery of square windows and a plain taffrail, "
        "two full gun decks of evenly spaced ports with the upper lids open, heavy black wales running the whole length, "
        "a deep keel and a square rudder, three tall masts with yards and tops, and a plain bow with a single anchor "
        "hanging at the cathead. One vessel only, no sails set. A 1.7 m human silhouette stands on the quarterdeck "
        "for scale, and a plain ruler with tick marks lies along the ground under the keel."
    ),
    "carrack": (
        "A medieval carrack in a broadside elevation that emphasises how unlike the later ships it is: a very high "
        "straight-sided hull with a round bilge, a rounded bow with a small beak, an enormous square sterncastle of "
        "three decks supported on the taffrail, a single deep keel, a high forecastle, two short masts with square "
        "yards, a low waist with a large square rudder under the counter and a capstan on the main deck. "
        "One vessel only, no sails set. A 1.7 m human silhouette stands on the sterncastle deck for scale, "
        "and a plain ruler with tick marks lies on the ground under the hull."
    ),
    "caravel": (
        "A caravel in a bow-quarter view from the starboard side, drawn so its identity reads: the high poop and the "
        "high forecastle at two different levels, the sharply raked stem with a fine entry, the wide flat transom "
        "overhanging the counter, the long narrow hull with a pronounced sheer, two masts with lateen yards, a "
        "tiller in a simple whipstaff binnacle aft, an anchor on the starboard bow and a capstan on the foredeck. "
        "One vessel only, no sails set, no water, no reflection. A 1.7 m human silhouette stands on the poop "
        "for scale, and a plain ruler with tick marks is laid flat on the ground beside the hull."
    ),
    "barge": (
        "A wide flat-bottomed cargo barge seen from the bow at a low angle, so the square bluff bow, the heavy "
        "transverse frames and the low flat bottom are the subject: a blunt stem with a heavy rubbing strake, riveted "
        "iron-shod flat bottom, three heavy transverse bulkheads visible inside, high solid bulwarks with a simple "
        "capstan and a cargo of barrels, square ends and no mast at all. "
        "One vessel only, hauled up on a slipway of wet sand with the ground under it, no water. "
        "A 1.7 m human silhouette stands in the bow on the sand for scale, "
        "and a plain ruler with tick marks lies on the sand beside the hull."
    ),
    "lighter": (
        "A stubby river lighter in a side elevation on a muddy slipway, so the flat bottom and the blunt working ends "
        "read clearly: a short fat hull with square ends, a low sheer, thick planking with iron clamps, a wide open "
        "hold with a plank hatch cover pushed back, big coarse oars shipped in the hull, a single mast stump amidships "
        "and a short towing mast lying along the gunwale. "
        "One vessel only, no water, no reflection, no second boat. A 1.7 m human silhouette stands on the mud beside "
        "the bow for scale, and a plain ruler with tick marks lies on the mud next to the hull."
    ),
    "pinnace": (
        "A small neat pinnace in a three-quarter view from above the port quarter, showing both the hull lines and "
        "the open interior: a fine rounded bow, a narrow clean stern, a low freeboard, three thwarts, a stern oarlock "
        "with its rowlocks, a single small mast with a furled sail, a tiny fore hatch and a painter's rope coiled in "
        "the bow. One vessel only, no water, no reflection. A 1.7 m human silhouette stands on the gunwale amidships "
        "for scale, and a plain ruler with tick marks lies on the ground beside the hull."
    ),
    "hulk": (
        "A derelict old hulk lying at anchor in shallow water: a heavy broad hull with a blunt bow and a blunt square "
        "stern, thick patched planking with tarred boards and new lighter planks spliced into the old ones, a sagging "
        "sheer, weed on the waterline, a broken mast stub with the rigging cut, a patched tarpaulin over the open hold, "
        "a collapsed capstan and an anchor hanging from the cathead. "
        "One vessel only. A 1.7 m human silhouette stands on the main deck for scale, "
        "and a plain ruler with tick marks lies on the flat shore in the foreground."
    ),
}

# per-id aspect ratio overrides
ASPECT_BY_ID = {
    "skiff": "4:3",
    "pinnace": "4:3",
    "lighter": "16:9",
    "barge": "16:9",
    "caravel": "16:9",
    "sloop": "16:9",
    "trawler": "16:9",
    "brigantine": "16:9",
    "frigate": "16:9",
}


def build_prompt(group, cid, subject, notes=""):
    """Return the final prompt string for one class."""
    if group == "ships":
        return SHIP_STYLE + " " + SHIP_PROMPTS[cid]
    tpl = TEMPLATES[group]
    scale = SCALE if group not in ("tiles", "ui", "weather") else ""
    body = tpl.format(subject=subject, notes=notes, scale=scale)
    return body


def aspect_for(group, cid):
    return ASPECT_BY_ID.get(cid, ASPECT.get(group, "1:1"))
