"""
Pie Menu module - Quick-access pie menu for common transforms.
Activated with Shift+Alt+<Key> (configurable in preferences).

The keymap is dynamically updated when the user changes the shortcut key
in addon preferences — no restart required.
"""

import bpy


class VIEW3D_MT_PIE_ItemTransform(bpy.types.Menu):
    """Item Transform Pro - Quick Access Pie Menu"""

    bl_label = "Item Transform"
    bl_idname = "VIEW3D_MT_PIE_item_transform"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # ---- PIE SLOTS (ordered: W, E, S, N, NW, NE, SW, SE) ----

        # WEST (Left) - Move to Ground/Center
        col = pie.column()
        col.scale_y = 1.2
        col.operator("object.item_transform_to_ground", text="To Ground", icon='IMPORT')
        col.operator("object.item_transform_to_center", text="To Center", icon='PIVOT_BOUNDBOX')

        # EAST (Right) - Reset/Apply
        col = pie.column()
        col.scale_y = 1.2
        col.operator("object.item_transform_reset", text="Reset", icon='LOOP_BACK')
        col.operator("object.item_transform_apply", text="Apply", icon='CHECKMARK')

        # SOUTH (Bottom) - Stack
        col = pie.column()
        col.scale_y = 1.2
        col.label(text="Stack", icon='SORTSIZE')
        row = col.row(align=True)
        op = row.operator("object.item_transform_stack", text="+Z")
        op.direction = 'Z'
        op = row.operator("object.item_transform_stack", text="-Z")
        op.direction = '-Z'
        row = col.row(align=True)
        op = row.operator("object.item_transform_stack", text="+X")
        op.direction = 'X'
        op = row.operator("object.item_transform_stack", text="+Y")
        op.direction = 'Y'

        # NORTH (Top) - Quick Scale
        col = pie.column()
        col.scale_y = 1.2
        col.label(text="Scale", icon='FULLSCREEN_ENTER')
        row = col.row(align=True)
        op = row.operator("object.item_transform_quick_scale", text="+", icon='ADD')
        op.direction = 'UP'
        op = row.operator("object.item_transform_quick_scale", text="-", icon='REMOVE')
        op.direction = 'DOWN'

        # NORTH-WEST (Top-Left) - Quick Move
        col = pie.column()
        col.scale_y = 1.2
        col.label(text="Move", icon='ORIENTATION_GLOBAL')
        row = col.row(align=True)
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_LEFT')
        op.direction = 'NEG_X'
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_RIGHT')
        op.direction = 'POS_X'
        row = col.row(align=True)
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_UP')
        op.direction = 'POS_Y'
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_DOWN')
        op.direction = 'NEG_Y'

        # NORTH-EAST (Top-Right) - Quick Rotate
        col = pie.column()
        col.scale_y = 1.2
        col.label(text="Rotate", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        row = col.row(align=True)
        for axis in ('X', 'Y', 'Z'):
            op = row.operator("object.item_transform_quick_rotate", text=axis)
            op.axis = axis
            op.direction = 'POSITIVE'

        # SOUTH-WEST (Bottom-Left) - Pivot
        col = pie.column()
        col.scale_y = 1.2
        col.label(text="Pivot", icon='PIVOT_BOUNDBOX')
        row = col.row(align=True)
        for ptype, label in [('CENTER', 'C'), ('BOTTOM', 'B'), ('TOP', 'T')]:
            op = row.operator("object.item_transform_set_pivot", text=label)
            op.pivot_type = ptype

        # SOUTH-EAST (Bottom-Right) - Snap & Arrays
        col = pie.column()
        col.scale_y = 1.2
        col.label(text="More", icon='TOOL_SETTINGS')
        col.operator("object.item_transform_copy", text="Copy XForm", icon='COPYDOWN')
        col.operator("object.item_transform_snap_to_surface", text="Snap Down", icon='SNAP_ON')
        col.operator("object.item_transform_mirror_placement", text="Mirror", icon='MOD_MIRROR')


# ============================================================
# Keymap Management
# ============================================================

addon_keymaps = []


def _get_preferred_key():
    """Read the pie menu shortcut key from addon preferences."""
    prefs = bpy.context.preferences.addons.get(__package__)
    if prefs and hasattr(prefs, 'preferences'):
        return prefs.preferences.pie_menu_key
    return 'T'


def _unregister_keymaps():
    """Remove all registered keymaps for this module."""
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def _register_keymaps():
    """Register the pie menu keymap with the current preferred key."""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return

    key = _get_preferred_key()

    km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(
        "wm.call_menu_pie",
        type=key,
        value='PRESS',
        shift=True,
        alt=True,
    )
    kmi.properties.name = "VIEW3D_MT_PIE_item_transform"
    addon_keymaps.append((km, kmi))


def refresh_keymap():
    """
    Public API: Remove existing keymap and re-register with current preference.
    Called by the preferences update callback for live shortcut changes.
    """
    _unregister_keymaps()
    _register_keymaps()


# ============================================================
# Registration
# ============================================================

def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_ItemTransform)
    _register_keymaps()


def unregister():
    _unregister_keymaps()
    bpy.utils.unregister_class(VIEW3D_MT_PIE_ItemTransform)
