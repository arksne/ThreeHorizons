import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(ROOT, "ART_ASSETS", "refs")
CLASSES = os.path.join(ROOT, "docs", "roadmap", "model-classes.json")

# User decision (2026-11-11): the archery family is not needed for this project.
SKIP = {
    "bow",
    "longbow",
    "shortbow",
    "crossbow",
    "arbalest",
}


def existing_ids():
    ids = set()
    for dirpath, _dirs, files in os.walk(REFS):
        for name in files:
            if name.lower().endswith(".png"):
                ids.add(os.path.splitext(name)[0])
    return ids


def main():
    data = json.load(open(CLASSES, encoding="utf-8"))
    have = existing_ids()
    missing = [c for c in data["classes"] if c["id"] not in have and c["id"] not in SKIP]
    groups = {}
    for c in missing:
        groups.setdefault(c["group"], []).append(c)
    out = []
    for group in sorted(groups):
        out.append("== %s (%d) ==" % (group, len(groups[group])))
        for c in groups[group]:
            out.append(
                "%s | %s | %s | %s | %s"
                % (c["id"], c.get("name", ""), c.get("sizeM", ""), c.get("triBudget", ""), c.get("usage", "")[:90])
            )
    text = "\n".join(out)
    with open(os.path.join(ROOT, "_missing.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    print("classes=%d have=%d missing=%d" % (len(data["classes"]), len(have), len(missing)))
    for group in sorted(groups):
        print("  %s=%d" % (group, len(groups[group])))


if __name__ == "__main__":
    main()
