"""
Panels module - UI panels for 3D Viewport sidebar (N-Panel) and Properties Editor.
Includes all feature sections: Quick Transform, Align, Stack, Randomize,
Pivot, Snap, Array, Presets, and Utilities.
"""

import bpy


# ============================================================
# Base Panel Mixin
# ============================================================

class ItemTransformPanelMixin:
    """Shared settings for all Item Transform panels."""

    bl_category = "Item Transform"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.object is not None


# ============================================================
# 3D Viewport Sidebar Panels (N-Panel)
# ============================================================

class VIEW3D_PT_ItemTransform_Main(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Item Transform Pro"
    bl_idname = "VIEW3D_PT_item_transform_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = set()  # Always open by default

    def draw(self, context):
        layout = self.layout
        layout.label(text="Professional Transform Toolkit", icon='ORIENTATION_GLOBAL')
        row = layout.row(align=True)
        row.label(text="Pie Menu: Shift+Alt+Key", icon='EVENT_OS')


class VIEW3D_PT_ItemTransform_QuickMove(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Quick Transform"
    bl_idname = "VIEW3D_PT_item_transform_quick"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout
        props = context.scene.item_transform

        # Factors
        col = layout.column(align=True)
        col.prop(props, "move_factor")
        col.prop(props, "rotate_factor")
        col.prop(props, "scale_factor")

        layout.separator()

        # Move
        box = layout.box()
        box.label(text="Move:", icon='ORIENTATION_GLOBAL')
        col = box.column(align=True)

        row = col.row(align=True)
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_LEFT')
        op.direction = 'NEG_X'
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_RIGHT')
        op.direction = 'POS_X'
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_UP')
        op.direction = 'POS_Y'
        op = row.operator("object.item_transform_quick_move", text="", icon='TRIA_DOWN')
        op.direction = 'NEG_Y'
        op = row.operator("object.item_transform_quick_move", text="Z+", icon='TRIA_UP_BAR')
        op.direction = 'POS_Z'
        op = row.operator("object.item_transform_quick_move", text="Z-", icon='TRIA_DOWN_BAR')
        op.direction = 'NEG_Z'

        # Rotate
        box = layout.box()
        box.label(text="Rotate:", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        row = box.row(align=True)
        for axis in ('X', 'Y', 'Z'):
            sub = row.column(align=True)
            op = sub.operator("object.item_transform_quick_rotate", text=f"+{axis}")
            op.axis = axis
            op.direction = 'POSITIVE'
            op = sub.operator("object.item_transform_quick_rotate", text=f"-{axis}")
            op.axis = axis
            op.direction = 'NEGATIVE'

        # Scale
        box = layout.box()
        box.label(text="Scale:", icon='FULLSCREEN_ENTER')
        row = box.row(align=True)
        op = row.operator("object.item_transform_quick_scale", text="Scale +", icon='ADD')
        op.direction = 'UP'
        op = row.operator("object.item_transform_quick_scale", text="Scale -", icon='REMOVE')
        op.direction = 'DOWN'


class VIEW3D_PT_ItemTransform_Align(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Align & Distribute"
    bl_idname = "VIEW3D_PT_item_transform_align"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout
        props = context.scene.item_transform

        # Align
        box = layout.box()
        box.label(text="Align Objects:", icon='SNAP_ON')
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(props, "align_axis", expand=True)
        row = col.row(align=True)
        row.prop(props, "align_mode", text="")
        op = col.operator("object.item_transform_align", icon='ALIGN_CENTER')
        op.axis = props.align_axis
        op.mode = props.align_mode

        layout.separator()

        # Distribute
        box = layout.box()
        box.label(text="Distribute Objects:", icon='ALIGN_JUSTIFY')
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(props, "distribute_axis", expand=True)
        row = col.row(align=True)
        row.prop(props, "distribute_mode", text="")
        op = col.operator("object.item_transform_distribute", icon='NORMALIZE_FCURVES')
        op.axis = props.distribute_axis
        op.mode = props.distribute_mode


class VIEW3D_PT_ItemTransform_Stack(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Stack Objects"
    bl_idname = "VIEW3D_PT_item_transform_stack"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout
        props = context.scene.item_transform

        col = layout.column(align=True)
        col.prop(props, "stack_direction")
        col.prop(props, "stack_gap")

        op = col.operator("object.item_transform_stack", icon='SORTSIZE')
        op.direction = props.stack_direction
        op.gap = props.stack_gap


class VIEW3D_PT_ItemTransform_Randomize(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Randomize"
    bl_idname = "VIEW3D_PT_item_transform_randomize"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout
        props = context.scene.item_transform

        col = layout.column(align=True)
        col.prop(props, "random_seed")

        col.separator()
        row = col.row(align=True)
        row.prop(props, "use_location", toggle=True)
        row.prop(props, "use_rotation", toggle=True)
        row.prop(props, "use_scale", toggle=True)

        if props.use_location:
            box = col.box()
            box.label(text="Location Range:")
            box.prop(props, "random_location", text="")

        if props.use_rotation:
            box = col.box()
            box.label(text="Rotation Range:")
            box.prop(props, "random_rotation", text="")

        if props.use_scale:
            box = col.box()
            box.label(text="Scale Range:")
            box.prop(props, "random_scale_uniform")
            row = box.row(align=True)
            row.prop(props, "random_scale_range", index=0, text="Min")
            row.prop(props, "random_scale_range", index=1, text="Max")

        col.separator()
        col.operator("object.item_transform_randomize", icon='MOD_NOISE')


class VIEW3D_PT_ItemTransform_Pivot(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Pivot & Origin"
    bl_idname = "VIEW3D_PT_item_transform_pivot"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        for ptype, label, icon in [
            ('CENTER', "Center", 'PIVOT_BOUNDBOX'),
            ('BOTTOM', "Bottom", 'TRIA_DOWN'),
            ('TOP', "Top", 'TRIA_UP'),
            ('CURSOR', "Cursor", 'PIVOT_CURSOR'),
            ('GEOMETRY', "Mass", 'PIVOT_MEDIAN'),
        ]:
            op = row.operator("object.item_transform_set_pivot", text=label, icon=icon)
            op.pivot_type = ptype


class VIEW3D_PT_ItemTransform_Snap(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Snap to Surface"
    bl_idname = "VIEW3D_PT_item_transform_snap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)

        # Snap to surface (raycast)
        box = col.box()
        box.label(text="Raycast Snap:", icon='SNAP_ON')
        row = box.row(align=True)
        row.operator("object.item_transform_snap_to_surface", text="Snap Down", icon='IMPORT')
        row.operator("object.item_transform_snap_to_active", text="To Active", icon='SNAP_FACE')

        box.operator("object.item_transform_drop_to_ground", text="Drop to Ground", icon='DOWNARROW_HLT')


class VIEW3D_PT_ItemTransform_Array(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Array Placement"
    bl_idname = "VIEW3D_PT_item_transform_array"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("object.item_transform_circular_array", icon='CURVE_BEZCIRCLE')
        col.operator("object.item_transform_grid_array", icon='MESH_GRID')
        col.operator("object.item_transform_linear_array", icon='EMPTY_SINGLE_ARROW')


class VIEW3D_PT_ItemTransform_Presets(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Transform Presets"
    bl_idname = "VIEW3D_PT_item_transform_presets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Preset list
        row = layout.row()
        row.template_list(
            "ITEM_TRANSFORM_UL_preset_list", "",
            scene, "item_transform_presets",
            scene, "item_transform_preset_index",
            rows=3,
        )

        # List controls (add/remove/move)
        col = row.column(align=True)
        col.operator("object.item_transform_save_preset", icon='ADD', text="")
        col.operator("object.item_transform_delete_preset", icon='REMOVE', text="")
        col.separator()
        op = col.operator("object.item_transform_move_preset", icon='TRIA_UP', text="")
        op.direction = 'UP'
        op = col.operator("object.item_transform_move_preset", icon='TRIA_DOWN', text="")
        op.direction = 'DOWN'

        # Apply button
        if len(scene.item_transform_presets) > 0:
            layout.separator()
            row = layout.row(align=True)
            row.operator("object.item_transform_apply_preset", text="Apply Preset", icon='PLAY')
            op = row.operator("object.item_transform_apply_preset", text="Add", icon='ADD')
            op.additive = True


class VIEW3D_PT_ItemTransform_Utilities(ItemTransformPanelMixin, bpy.types.Panel):
    bl_label = "Utilities"
    bl_idname = "VIEW3D_PT_item_transform_utilities"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_item_transform_main"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)

        # Transform operations
        row = col.row(align=True)
        row.operator("object.item_transform_to_ground", text="To Ground", icon='IMPORT')
        row.operator("object.item_transform_to_center", text="To Center", icon='PIVOT_BOUNDBOX')

        row = col.row(align=True)
        row.operator("object.item_transform_reset", text="Reset", icon='LOOP_BACK')
        row.operator("object.item_transform_apply", text="Apply", icon='CHECKMARK')

        col.separator()

        # Copy & Mirror
        row = col.row(align=True)
        row.operator("object.item_transform_copy", text="Copy Transform", icon='COPYDOWN')
        row.operator("object.item_transform_mirror_placement", text="Mirror", icon='MOD_MIRROR')

        col.separator()

        # Cleanup
        row = col.row(align=True)
        row.operator("object.item_transform_purge", text="Purge Data", icon='TRASH')
        row.operator("object.item_transform_delete_hierarchy", text="Delete All", icon='X')

        col.operator("object.item_transform_duplicate_linked", text="Duplicate Linked", icon='DUPLICATE')


# ============================================================
# Properties Editor Panel
# ============================================================

class OBJECT_PT_ItemTransform_Properties(bpy.types.Panel):
    bl_label = "Item Transform Pro"
    bl_idname = "OBJECT_PT_item_transform_props"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        props = context.scene.item_transform
        obj = context.object

        # Object info
        box = layout.box()
        box.label(text=f"Active: {obj.name}", icon='OBJECT_DATA')
        col = box.column(align=True)
        col.prop(obj, "location")
        col.prop(obj, "rotation_euler", text="Rotation")
        col.prop(obj, "scale")
        col.prop(obj, "dimensions")

        layout.separator()

        # Quick access buttons
        box = layout.box()
        box.label(text="Quick Actions:", icon='TOOL_SETTINGS')
        col = box.column(align=True)

        row = col.row(align=True)
        row.operator("object.item_transform_to_ground", text="Ground", icon='IMPORT')
        row.operator("object.item_transform_to_center", text="Center", icon='PIVOT_BOUNDBOX')
        row.operator("object.item_transform_reset", text="Reset", icon='LOOP_BACK')
        row.operator("object.item_transform_apply", text="Apply", icon='CHECKMARK')

        col.separator()
        row = col.row(align=True)
        row.operator("object.item_transform_snap_to_surface", text="Snap", icon='SNAP_ON')
        row.operator("object.item_transform_drop_to_ground", text="Drop", icon='DOWNARROW_HLT')

        layout.label(text="Full controls in 3D Viewport > N-Panel", icon='INFO')


# ============================================================
# Registration
# ============================================================

classes = (
    # 3D Viewport panels
    VIEW3D_PT_ItemTransform_Main,
    VIEW3D_PT_ItemTransform_QuickMove,
    VIEW3D_PT_ItemTransform_Align,
    VIEW3D_PT_ItemTransform_Stack,
    VIEW3D_PT_ItemTransform_Randomize,
    VIEW3D_PT_ItemTransform_Pivot,
    VIEW3D_PT_ItemTransform_Snap,
    VIEW3D_PT_ItemTransform_Array,
    VIEW3D_PT_ItemTransform_Presets,
    VIEW3D_PT_ItemTransform_Utilities,
    # Properties panel
    OBJECT_PT_ItemTransform_Properties,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
