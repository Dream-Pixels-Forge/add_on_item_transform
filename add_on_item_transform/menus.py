"""
Header Menus module - Adds an "Item Transform" sub-menu to the Object menu
in the 3D Viewport header for discoverability.

Accessible via: 3D Viewport > Object > Item Transform
"""

import bpy


# ============================================================
# Sub-menus
# ============================================================

class VIEW3D_MT_ItemTransform_Quick(bpy.types.Menu):
    bl_label = "Quick Transform"
    bl_idname = "VIEW3D_MT_item_transform_quick"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Move", icon='ORIENTATION_GLOBAL')
        for direction, label in [
            ('POS_X', "+X"), ('NEG_X', "-X"),
            ('POS_Y', "+Y"), ('NEG_Y', "-Y"),
            ('POS_Z', "+Z"), ('NEG_Z', "-Z"),
        ]:
            op = layout.operator("object.item_transform_quick_move", text=f"Move {label}")
            op.direction = direction

        layout.separator()
        layout.label(text="Rotate", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        for axis in ('X', 'Y', 'Z'):
            op = layout.operator("object.item_transform_quick_rotate", text=f"Rotate +{axis}")
            op.axis = axis
            op.direction = 'POSITIVE'
            op = layout.operator("object.item_transform_quick_rotate", text=f"Rotate -{axis}")
            op.axis = axis
            op.direction = 'NEGATIVE'

        layout.separator()
        layout.label(text="Scale", icon='FULLSCREEN_ENTER')
        op = layout.operator("object.item_transform_quick_scale", text="Scale Up")
        op.direction = 'UP'
        op = layout.operator("object.item_transform_quick_scale", text="Scale Down")
        op.direction = 'DOWN'


class VIEW3D_MT_ItemTransform_Align(bpy.types.Menu):
    bl_label = "Align & Distribute"
    bl_idname = "VIEW3D_MT_item_transform_align"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Align", icon='SNAP_ON')
        for axis in ('X', 'Y', 'Z'):
            for mode, label in [('MIN', 'Min'), ('CENTER', 'Center'), ('MAX', 'Max')]:
                op = layout.operator(
                    "object.item_transform_align",
                    text=f"Align {axis} {label}",
                )
                op.axis = axis
                op.mode = mode

        layout.separator()
        layout.label(text="Distribute", icon='ALIGN_JUSTIFY')
        for axis in ('X', 'Y', 'Z'):
            op = layout.operator(
                "object.item_transform_distribute",
                text=f"Distribute {axis} (Even)",
            )
            op.axis = axis
            op.mode = 'EVEN'


class VIEW3D_MT_ItemTransform_Array(bpy.types.Menu):
    bl_label = "Array Placement"
    bl_idname = "VIEW3D_MT_item_transform_array"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.item_transform_circular_array", icon='CURVE_BEZCIRCLE')
        layout.operator("object.item_transform_grid_array", icon='MESH_GRID')
        layout.operator("object.item_transform_linear_array", icon='EMPTY_SINGLE_ARROW')


class VIEW3D_MT_ItemTransform_Snap(bpy.types.Menu):
    bl_label = "Snap to Surface"
    bl_idname = "VIEW3D_MT_item_transform_snap"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.item_transform_snap_to_surface", icon='SNAP_ON')
        layout.operator("object.item_transform_snap_to_active", icon='SNAP_FACE')
        layout.operator("object.item_transform_drop_to_ground", icon='IMPORT')


class VIEW3D_MT_ItemTransform_Pivot(bpy.types.Menu):
    bl_label = "Pivot & Origin"
    bl_idname = "VIEW3D_MT_item_transform_pivot"

    def draw(self, context):
        layout = self.layout
        for ptype, label, icon in [
            ('CENTER', "Origin to Center", 'PIVOT_BOUNDBOX'),
            ('BOTTOM', "Origin to Bottom", 'TRIA_DOWN'),
            ('TOP', "Origin to Top", 'TRIA_UP'),
            ('CURSOR', "Origin to Cursor", 'PIVOT_CURSOR'),
            ('GEOMETRY', "Origin to Geometry", 'PIVOT_MEDIAN'),
        ]:
            op = layout.operator("object.item_transform_set_pivot", text=label, icon=icon)
            op.pivot_type = ptype


# ============================================================
# Main Menu (appended to Object menu)
# ============================================================

class VIEW3D_MT_ItemTransform_Main(bpy.types.Menu):
    """Item Transform Pro - Main header menu"""

    bl_label = "Item Transform"
    bl_idname = "VIEW3D_MT_item_transform_main"

    def draw(self, context):
        layout = self.layout

        # Sub-menus
        layout.menu("VIEW3D_MT_item_transform_quick", icon='ORIENTATION_GLOBAL')
        layout.menu("VIEW3D_MT_item_transform_align", icon='SNAP_ON')
        layout.menu("VIEW3D_MT_item_transform_array", icon='MOD_ARRAY')
        layout.menu("VIEW3D_MT_item_transform_snap", icon='SNAP_FACE')
        layout.menu("VIEW3D_MT_item_transform_pivot", icon='PIVOT_BOUNDBOX')

        layout.separator()

        # Direct utilities
        layout.label(text="Utilities", icon='TOOL_SETTINGS')
        layout.operator("object.item_transform_to_ground", icon='IMPORT')
        layout.operator("object.item_transform_to_center", icon='PIVOT_BOUNDBOX')
        layout.operator("object.item_transform_reset", icon='LOOP_BACK')
        layout.operator("object.item_transform_apply", icon='CHECKMARK')

        layout.separator()

        layout.operator("object.item_transform_copy", icon='COPYDOWN')
        layout.operator("object.item_transform_mirror_placement", icon='MOD_MIRROR')
        layout.operator("object.item_transform_duplicate_linked", icon='DUPLICATE')

        layout.separator()

        # Presets
        layout.label(text="Presets", icon='BOOKMARKS')
        layout.operator("object.item_transform_save_preset", icon='ADD')
        layout.operator("object.item_transform_apply_preset", icon='PLAY')

        layout.separator()

        # Cleanup
        layout.operator("object.item_transform_purge", icon='TRASH')
        layout.operator("object.item_transform_delete_hierarchy", icon='X')


# ============================================================
# Draw function appended to VIEW3D_MT_object
# ============================================================

def draw_item_transform_menu(self, context):
    """Appended to the Object menu in the 3D Viewport header."""
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_item_transform_main", icon='OBJECT_DATA')


# ============================================================
# Registration
# ============================================================

classes = (
    VIEW3D_MT_ItemTransform_Quick,
    VIEW3D_MT_ItemTransform_Align,
    VIEW3D_MT_ItemTransform_Array,
    VIEW3D_MT_ItemTransform_Snap,
    VIEW3D_MT_ItemTransform_Pivot,
    VIEW3D_MT_ItemTransform_Main,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(draw_item_transform_menu)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(draw_item_transform_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
