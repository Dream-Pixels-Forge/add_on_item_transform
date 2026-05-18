"""
Transform Presets operators - Save, load, and apply named transform presets.
Presets are stored per-scene in a CollectionProperty, allowing quick recall
of frequently used transform configurations.
"""

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
)


# ============================================================
# Preset Data PropertyGroup
# ============================================================

class ITEM_TRANSFORM_PresetItem(bpy.types.PropertyGroup):
    """A single saved transform preset."""

    name: StringProperty(
        name="Preset Name",
        default="Untitled",
    )

    location: FloatVectorProperty(
        name="Location",
        size=3,
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
    )

    rotation: FloatVectorProperty(
        name="Rotation",
        size=3,
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
    )

    scale: FloatVectorProperty(
        name="Scale",
        size=3,
        default=(1.0, 1.0, 1.0),
        subtype='XYZ',
    )

    has_location: BoolProperty(name="Has Location", default=True)
    has_rotation: BoolProperty(name="Has Rotation", default=True)
    has_scale: BoolProperty(name="Has Scale", default=True)


# ============================================================
# Operators
# ============================================================

class OBJECT_OT_SaveTransformPreset(bpy.types.Operator):
    """Save the active object's transform as a named preset"""

    bl_idname = "object.item_transform_save_preset"
    bl_label = "Save Transform Preset"
    bl_options = {'REGISTER', 'UNDO'}

    preset_name: StringProperty(
        name="Name",
        description="Name for the preset",
        default="My Preset",
    )

    save_location: BoolProperty(name="Save Location", default=True)
    save_rotation: BoolProperty(name="Save Rotation", default=True)
    save_scale: BoolProperty(name="Save Scale", default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset_name")
        row = layout.row(align=True)
        row.prop(self, "save_location", toggle=True)
        row.prop(self, "save_rotation", toggle=True)
        row.prop(self, "save_scale", toggle=True)

    def execute(self, context):
        obj = context.active_object
        presets = context.scene.item_transform_presets

        # Check for existing preset with same name and overwrite
        existing = None
        for preset in presets:
            if preset.name == self.preset_name:
                existing = preset
                break

        if existing:
            preset = existing
        else:
            preset = presets.add()

        preset.name = self.preset_name
        preset.has_location = self.save_location
        preset.has_rotation = self.save_rotation
        preset.has_scale = self.save_scale

        if self.save_location:
            preset.location = obj.location.copy()
        if self.save_rotation:
            preset.rotation = obj.rotation_euler.copy()
        if self.save_scale:
            preset.scale = obj.scale.copy()

        # Update active index
        context.scene.item_transform_preset_index = len(presets) - 1

        action = "Updated" if existing else "Saved"
        self.report({'INFO'}, f"{action} preset: '{self.preset_name}'")
        return {'FINISHED'}


class OBJECT_OT_ApplyTransformPreset(bpy.types.Operator):
    """Apply a saved transform preset to selected objects"""

    bl_idname = "object.item_transform_apply_preset"
    bl_label = "Apply Transform Preset"
    bl_options = {'REGISTER', 'UNDO'}

    preset_index: IntProperty(
        name="Preset Index",
        description="Index of the preset to apply",
        default=-1,
    )

    apply_location: BoolProperty(name="Apply Location", default=True)
    apply_rotation: BoolProperty(name="Apply Rotation", default=True)
    apply_scale: BoolProperty(name="Apply Scale", default=True)

    additive: BoolProperty(
        name="Additive",
        description="Add preset values to current transform instead of replacing",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return (
            context.selected_objects
            and context.mode == 'OBJECT'
            and len(context.scene.item_transform_presets) > 0
        )

    def execute(self, context):
        presets = context.scene.item_transform_presets

        # Use specified index or the scene's active index
        idx = self.preset_index
        if idx < 0:
            idx = context.scene.item_transform_preset_index

        if idx < 0 or idx >= len(presets):
            self.report({'ERROR'}, "No valid preset selected")
            return {'CANCELLED'}

        preset = presets[idx]
        applied = 0

        for obj in context.selected_objects:
            if self.apply_location and preset.has_location:
                if self.additive:
                    obj.location.x += preset.location[0]
                    obj.location.y += preset.location[1]
                    obj.location.z += preset.location[2]
                else:
                    obj.location = preset.location[:]

            if self.apply_rotation and preset.has_rotation:
                if self.additive:
                    obj.rotation_euler.x += preset.rotation[0]
                    obj.rotation_euler.y += preset.rotation[1]
                    obj.rotation_euler.z += preset.rotation[2]
                else:
                    obj.rotation_euler = preset.rotation[:]

            if self.apply_scale and preset.has_scale:
                if self.additive:
                    obj.scale.x *= preset.scale[0]
                    obj.scale.y *= preset.scale[1]
                    obj.scale.z *= preset.scale[2]
                else:
                    obj.scale = preset.scale[:]

            applied += 1

        self.report(
            {'INFO'},
            f"Applied preset '{preset.name}' to {applied} object(s)"
            + (" (additive)" if self.additive else ""),
        )
        return {'FINISHED'}


class OBJECT_OT_DeleteTransformPreset(bpy.types.Operator):
    """Delete the selected transform preset"""

    bl_idname = "object.item_transform_delete_preset"
    bl_label = "Delete Preset"
    bl_options = {'REGISTER', 'UNDO'}

    preset_index: IntProperty(
        name="Preset Index",
        default=-1,
    )

    @classmethod
    def poll(cls, context):
        return len(context.scene.item_transform_presets) > 0

    def execute(self, context):
        presets = context.scene.item_transform_presets
        idx = self.preset_index
        if idx < 0:
            idx = context.scene.item_transform_preset_index

        if idx < 0 or idx >= len(presets):
            self.report({'ERROR'}, "No valid preset to delete")
            return {'CANCELLED'}

        name = presets[idx].name
        presets.remove(idx)

        # Adjust active index
        if context.scene.item_transform_preset_index >= len(presets):
            context.scene.item_transform_preset_index = max(0, len(presets) - 1)

        self.report({'INFO'}, f"Deleted preset: '{name}'")
        return {'FINISHED'}


class OBJECT_OT_MoveTransformPreset(bpy.types.Operator):
    """Move a preset up or down in the list"""

    bl_idname = "object.item_transform_move_preset"
    bl_label = "Move Preset"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        items=[
            ('UP', "Up", "Move preset up"),
            ('DOWN', "Down", "Move preset down"),
        ],
    )

    @classmethod
    def poll(cls, context):
        return len(context.scene.item_transform_presets) > 1

    def execute(self, context):
        presets = context.scene.item_transform_presets
        idx = context.scene.item_transform_preset_index

        if self.direction == 'UP' and idx > 0:
            presets.move(idx, idx - 1)
            context.scene.item_transform_preset_index -= 1
        elif self.direction == 'DOWN' and idx < len(presets) - 1:
            presets.move(idx, idx + 1)
            context.scene.item_transform_preset_index += 1
        else:
            return {'CANCELLED'}

        return {'FINISHED'}


# ============================================================
# UI List for Presets
# ============================================================

class ITEM_TRANSFORM_UL_PresetList(bpy.types.UIList):
    """Custom UI list for transform presets."""

    bl_idname = "ITEM_TRANSFORM_UL_preset_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "name", text="", emboss=False, icon='BOOKMARKS')

            # Show which components are stored
            sub = row.row(align=True)
            sub.scale_x = 0.5
            if item.has_location:
                sub.label(text="L")
            if item.has_rotation:
                sub.label(text="R")
            if item.has_scale:
                sub.label(text="S")

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=item.name, icon='BOOKMARKS')


# ============================================================
# Registration
# ============================================================

classes = (
    ITEM_TRANSFORM_PresetItem,
    ITEM_TRANSFORM_UL_PresetList,
    OBJECT_OT_SaveTransformPreset,
    OBJECT_OT_ApplyTransformPreset,
    OBJECT_OT_DeleteTransformPreset,
    OBJECT_OT_MoveTransformPreset,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.item_transform_presets = bpy.props.CollectionProperty(
        type=ITEM_TRANSFORM_PresetItem,
        name="Transform Presets",
    )
    bpy.types.Scene.item_transform_preset_index = bpy.props.IntProperty(
        name="Active Preset Index",
        default=0,
    )


def unregister():
    del bpy.types.Scene.item_transform_preset_index
    del bpy.types.Scene.item_transform_presets

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
