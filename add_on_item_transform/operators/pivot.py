"""
Pivot operators - Set object origin/pivot to various positions.
"""

import bpy
from bpy.props import EnumProperty
from mathutils import Vector


class OBJECT_OT_SetPivot(bpy.types.Operator):
    """Set the origin (pivot point) of the active object"""

    bl_idname = "object.item_transform_set_pivot"
    bl_label = "Set Pivot"
    bl_options = {'REGISTER', 'UNDO'}

    pivot_type: EnumProperty(
        name="Pivot Type",
        items=[
            ('CENTER', "Center", "Set origin to bounding box center"),
            ('BOTTOM', "Bottom", "Set origin to bounding box bottom center"),
            ('TOP', "Top", "Set origin to bounding box top center"),
            ('CURSOR', "Cursor", "Set origin to 3D cursor"),
            ('GEOMETRY', "Geometry", "Set origin to center of geometry mass"),
        ],
        default='CENTER',
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.mode == 'OBJECT'

    def execute(self, context):
        obj = context.active_object

        if self.pivot_type == 'CENTER':
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        elif self.pivot_type == 'GEOMETRY':
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        elif self.pivot_type == 'CURSOR':
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        elif self.pivot_type in ('BOTTOM', 'TOP'):
            # Save cursor
            cursor_loc = context.scene.cursor.location.copy()

            # Get world-space bounds
            bounds = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

            if self.pivot_type == 'BOTTOM':
                target_z = min(v.z for v in bounds)
            else:
                target_z = max(v.z for v in bounds)

            # Set cursor to target, keeping XY at object center
            center_x = (min(v.x for v in bounds) + max(v.x for v in bounds)) / 2.0
            center_y = (min(v.y for v in bounds) + max(v.y for v in bounds)) / 2.0

            context.scene.cursor.location = Vector((center_x, center_y, target_z))
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

            # Restore cursor
            context.scene.cursor.location = cursor_loc

        self.report({'INFO'}, f"Set pivot to {self.pivot_type.lower()}")
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_SetPivot,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
