"""
Stack operators - Stack objects along an axis based on bounding boxes.
"""

import bpy
from bpy.props import EnumProperty, FloatProperty

from ..utils import axis_index, get_bounds_on_axis


class OBJECT_OT_StackObjects(bpy.types.Operator):
    """Stack selected objects along an axis with optional gap"""

    bl_idname = "object.item_transform_stack"
    bl_label = "Stack Objects"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        items=[
            ('X', "+X", "Stack along positive X"),
            ('-X', "-X", "Stack along negative X"),
            ('Y', "+Y", "Stack along positive Y"),
            ('-Y', "-Y", "Stack along negative Y"),
            ('Z', "+Z", "Stack along positive Z"),
            ('-Z', "-Z", "Stack along negative Z"),
        ],
        default='Z',
    )

    gap: FloatProperty(
        name="Gap",
        description="Space between stacked objects",
        default=0.0,
        soft_min=-10.0,
        soft_max=10.0,
        subtype='DISTANCE',
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 2 and context.mode == 'OBJECT'

    def execute(self, context):
        props = context.scene.item_transform
        objects = list(context.selected_objects)

        # Use operator property if set, otherwise use scene property
        direction = self.direction if self.direction else props.stack_direction
        gap = self.gap if self.gap != 0.0 else props.stack_gap

        if len(objects) < 2:
            self.report({'ERROR'}, "Select at least 2 objects to stack")
            return {'CANCELLED'}

        # Determine axis and sign
        axis_map = {'X': 0, '-X': 0, 'Y': 1, '-Y': 1, 'Z': 2, '-Z': 2}
        axis_idx = axis_map[direction]
        positive = not direction.startswith('-')

        # Sort objects by position on axis
        objects.sort(
            key=lambda o: o.location[axis_idx],
            reverse=not positive,
        )

        # Stack each object after the first
        for i in range(1, len(objects)):
            prev_obj = objects[i - 1]
            curr_obj = objects[i]

            prev_min, prev_max = get_bounds_on_axis(prev_obj, axis_idx)
            curr_min, curr_max = get_bounds_on_axis(curr_obj, axis_idx)
            curr_size = curr_max - curr_min

            # Calculate where the current object's min/max should be
            if positive:
                # Place current object's min at prev object's max + gap
                target_min = prev_max + gap
                offset = target_min - curr_min
            else:
                # Place current object's max at prev object's min - gap
                target_max = prev_min - gap
                offset = target_max - curr_max

            curr_obj.location[axis_idx] += offset

        self.report({'INFO'}, f"Stacked {len(objects)} objects along {direction}")
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_StackObjects,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
