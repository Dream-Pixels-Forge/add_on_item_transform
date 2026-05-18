"""
Align operators - Align objects along axes using various reference points.
"""

import bpy
from bpy.props import EnumProperty

from ..utils import axis_index, get_bound_value


class OBJECT_OT_AlignObjects(bpy.types.Operator):
    """Align selected objects along an axis"""

    bl_idname = "object.item_transform_align"
    bl_label = "Align Objects"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "Align on X axis"),
            ('Y', "Y", "Align on Y axis"),
            ('Z', "Z", "Align on Z axis"),
        ],
        default='X',
    )

    mode: EnumProperty(
        name="Mode",
        items=[
            ('MIN', "Min", "Align to minimum bound"),
            ('CENTER', "Center", "Align to center"),
            ('MAX', "Max", "Align to maximum bound"),
            ('CURSOR', "Cursor", "Align to 3D cursor"),
            ('ACTIVE', "Active", "Align to active object"),
        ],
        default='CENTER',
    )

    @classmethod
    def poll(cls, context):
        return (
            context.selected_objects
            and context.mode == 'OBJECT'
        )

    def execute(self, context):
        objects = context.selected_objects
        axis_idx = axis_index(self.axis)

        # Determine target value
        if self.mode == 'CURSOR':
            target = context.scene.cursor.location[axis_idx]
        elif self.mode == 'ACTIVE':
            active = context.active_object
            if not active:
                self.report({'ERROR'}, "No active object for alignment reference")
                return {'CANCELLED'}
            target = get_bound_value(active, axis_idx, 'CENTER')
        else:
            # Use the collective min/max/center of all selected
            all_values = [get_bound_value(obj, axis_idx, self.mode) for obj in objects]

            if self.mode == 'MIN':
                target = min(all_values)
            elif self.mode == 'MAX':
                target = max(all_values)
            else:  # CENTER
                target = (min(all_values) + max(all_values)) / 2.0

        # Apply alignment
        for obj in objects:
            ref_mode = self.mode if self.mode in ('MIN', 'MAX', 'CENTER') else 'CENTER'
            current = get_bound_value(obj, axis_idx, ref_mode)
            offset = target - current
            obj.location[axis_idx] += offset

        self.report({'INFO'}, f"Aligned {len(objects)} object(s) on {self.axis} ({self.mode})")
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_AlignObjects,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
