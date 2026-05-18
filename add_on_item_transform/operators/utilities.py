"""
Utility operators - Common transform helpers and cleanup tools.
"""

import bpy
from bpy.props import BoolProperty

from ..utils import get_world_bounds, axis_index


class OBJECT_OT_MoveToGround(bpy.types.Operator):
    """Move selected objects so their lowest point touches Z=0"""

    bl_idname = "object.item_transform_to_ground"
    bl_label = "Move to Ground"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        count = 0
        for obj in context.selected_objects:
            bounds = get_world_bounds(obj)
            if len(bounds) <= 1 and not hasattr(obj, 'bound_box'):
                continue
            min_z = min(v.z for v in bounds)
            obj.location.z -= min_z
            count += 1

        if count == 0:
            self.report({'WARNING'}, "No valid objects to move to ground")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Moved {count} object(s) to ground")
        return {'FINISHED'}


class OBJECT_OT_MoveToCenter(bpy.types.Operator):
    """Move selected objects to world origin (0, 0, 0)"""

    bl_idname = "object.item_transform_to_center"
    bl_label = "Move to Center"
    bl_options = {'REGISTER', 'UNDO'}

    keep_z: BoolProperty(
        name="Keep Z",
        description="Preserve the Z position",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        for obj in context.selected_objects:
            if self.keep_z:
                obj.location.x = 0.0
                obj.location.y = 0.0
            else:
                obj.location = (0.0, 0.0, 0.0)

        self.report({'INFO'}, f"Centered {len(context.selected_objects)} object(s)")
        return {'FINISHED'}


class OBJECT_OT_ResetTransforms(bpy.types.Operator):
    """Reset location, rotation, and/or scale to defaults"""

    bl_idname = "object.item_transform_reset"
    bl_label = "Reset Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    reset_location: BoolProperty(name="Location", default=True)
    reset_rotation: BoolProperty(name="Rotation", default=True)
    reset_scale: BoolProperty(name="Scale", default=True)

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        for obj in context.selected_objects:
            if self.reset_location:
                obj.location = (0.0, 0.0, 0.0)
            if self.reset_rotation:
                obj.rotation_euler = (0.0, 0.0, 0.0)
            if self.reset_scale:
                obj.scale = (1.0, 1.0, 1.0)

        self.report({'INFO'}, f"Reset transforms on {len(context.selected_objects)} object(s)")
        return {'FINISHED'}


class OBJECT_OT_ApplyTransform(bpy.types.Operator):
    """Apply all transformations (location, rotation, scale)"""

    bl_idname = "object.item_transform_apply"
    bl_label = "Apply Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    apply_location: BoolProperty(name="Location", default=True)
    apply_rotation: BoolProperty(name="Rotation", default=True)
    apply_scale: BoolProperty(name="Scale", default=True)

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.object.transform_apply(
            location=self.apply_location,
            rotation=self.apply_rotation,
            scale=self.apply_scale,
        )
        self.report({'INFO'}, "Applied transforms")
        return {'FINISHED'}


class OBJECT_OT_CopyTransform(bpy.types.Operator):
    """Copy transform from active object to all other selected objects"""

    bl_idname = "object.item_transform_copy"
    bl_label = "Copy Transform"
    bl_options = {'REGISTER', 'UNDO'}

    copy_location: BoolProperty(name="Location", default=True)
    copy_rotation: BoolProperty(name="Rotation", default=True)
    copy_scale: BoolProperty(name="Scale", default=True)

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and len(context.selected_objects) >= 2
            and context.mode == 'OBJECT'
        )

    def execute(self, context):
        source = context.active_object
        targets = [o for o in context.selected_objects if o != source]

        for obj in targets:
            if self.copy_location:
                obj.location = source.location.copy()
            if self.copy_rotation:
                obj.rotation_euler = source.rotation_euler.copy()
            if self.copy_scale:
                obj.scale = source.scale.copy()

        self.report({'INFO'}, f"Copied transform to {len(targets)} object(s)")
        return {'FINISHED'}


class OBJECT_OT_PurgeData(bpy.types.Operator):
    """Purge all unused/orphaned data-blocks recursively"""

    bl_idname = "object.item_transform_purge"
    bl_label = "Purge Unused Data"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.outliner.orphans_purge(do_recursive=True)
        self.report({'INFO'}, "Purged orphaned data")
        return {'FINISHED'}


class OBJECT_OT_DeleteHierarchy(bpy.types.Operator):
    """Delete selected objects and all their children recursively"""

    bl_idname = "object.item_transform_delete_hierarchy"
    bl_label = "Delete Hierarchy"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        # Collect all objects to delete (parents + children)
        to_delete = set()
        for obj in context.selected_objects:
            to_delete.add(obj)
            self._collect_children(obj, to_delete)

        # Delete all collected objects
        for obj in to_delete:
            bpy.data.objects.remove(obj, do_unlink=True)

        self.report({'INFO'}, f"Deleted {len(to_delete)} object(s)")
        return {'FINISHED'}

    def _collect_children(self, obj, collection):
        """Recursively collect all children."""
        for child in obj.children:
            collection.add(child)
            self._collect_children(child, collection)


class OBJECT_OT_DuplicateLinked(bpy.types.Operator):
    """Create a linked duplicate (instance) of selected objects"""

    bl_idname = "object.item_transform_duplicate_linked"
    bl_label = "Duplicate Linked"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.object.duplicate(linked=True)
        self.report({'INFO'}, "Created linked duplicate(s)")
        return {'FINISHED'}


class OBJECT_OT_MirrorPlacement(bpy.types.Operator):
    """Mirror object placement across an axis through the world origin or cursor"""

    bl_idname = "object.item_transform_mirror_placement"
    bl_label = "Mirror Placement"
    bl_options = {'REGISTER', 'UNDO'}

    mirror_axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "Mirror across YZ plane"),
            ('Y', "Y", "Mirror across XZ plane"),
            ('Z', "Z", "Mirror across XY plane"),
        ],
        default='X',
    )

    use_cursor: BoolProperty(
        name="Use Cursor",
        description="Mirror relative to 3D cursor instead of world origin",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        axis_idx = axis_index(self.mirror_axis)
        pivot = context.scene.cursor.location[axis_idx] if self.use_cursor else 0.0

        for obj in context.selected_objects:
            obj.location[axis_idx] = 2.0 * pivot - obj.location[axis_idx]

        self.report(
            {'INFO'},
            f"Mirrored {len(context.selected_objects)} object(s) on {self.mirror_axis}",
        )
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_MoveToGround,
    OBJECT_OT_MoveToCenter,
    OBJECT_OT_ResetTransforms,
    OBJECT_OT_ApplyTransform,
    OBJECT_OT_CopyTransform,
    OBJECT_OT_PurgeData,
    OBJECT_OT_DeleteHierarchy,
    OBJECT_OT_DuplicateLinked,
    OBJECT_OT_MirrorPlacement,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
