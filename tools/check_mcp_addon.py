"""Проверка: видит ли портативный Blender аддон MCP for Blender и включается ли он."""
import addon_utils

mods = [m.__name__ for m in addon_utils.modules() if "mcp" in m.__name__.lower()]
print("MCP_ADDONS_FOUND:", mods)

try:
    bpy.ops.preferences.addon_enable(module="blender_mcp")
    print("MCP_ENABLE_OK")
except Exception as e:
    print("MCP_ENABLE_FAIL:", type(e).__name__, e)

try:
    import blender_mcp
    print("MCP_IMPORT_OK", getattr(blender_mcp, "__file__", "?"))
except Exception as e:
    print("MCP_IMPORT_FAIL:", type(e).__name__, e)

# что умеет аддон
try:
    import blender_mcp
    ops = [o for o in dir(blender_mcp) if not o.startswith("_")]
    print("MCP_MODULE_ATTRS:", ops[:25])
except Exception:
    pass
