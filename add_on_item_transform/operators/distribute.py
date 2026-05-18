"""
Distribute operators - Evenly distribute objects along an axis.
"""

import bpy
from bpy.props import EnumProperty
from mathutils import Vector


def _get_bounds_on_axis(obj, axis_idx):
    """Return (min, max) of the object's bounding box on the given axis."""
    bounds = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    values = [v[axis_idx] for v in bounds]
    return min(values), max(values)


class OBJECT_OT_DistributeObjects(bpy.types.Operator):
    """Distribute selected objects evenly along an axis"""

    bl_idname = "object.item_transform_distribute"
    bl_label = "Distribute Objects"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "Distribute along X"),
            ('Y', "Y", "Distribute along Y"),
            ('Z', "Z", "Distribute along Z"),
        ],
        default='X',
    )

    mode: EnumProperty(
        name="Mode",
        items=[
            ('EVEN', "Even Spacing", "Equal gaps between objects"),
            ('CENTERS', "Even Centers", "Equal distance between centers"),
        ],
        default='EVEN',
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 3 and context.mode == 'OBJECT'

    def execute(self, context):
        objects = list(context.selected_objects)
        axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[self.axis]

        if len(objects) < 3:
            self.report({'WARNING'}, "Need at least 3 objects to distribute")
            return {'CANCELLED'}

        # Sort objects by their center position on the axis
        objects.sort(key=lambda o: o.location[axis_idx])

        if self.mode == 'CENTERS':
            # Distribute centers evenly between first and last
            first_pos = objects[0].location[axis_idx]
            last_pos = objects[-1].location[axis_idx]
            total_dist = last_pos - first_pos

            if total_dist == 0:
                self.report({'WARNING'}, "Objects are at the same position")
                return {'CANCELLED'}

            step = total_dist / (len(objects) - 1)
            for i, obj in enumerate(objects[1:-1], start=1):
                obj.location[axis_idx] = first_pos + step * i

        else:  # EVEN spacing
            # Calculate total available space and total object sizes
            first_min, first_max = _get_bounds_on_axis(objects[0], axis_idx)
            last_min, last_max = _get_bounds_on_axis(objects[-1], axis_idx)

            total_span = last_max - first_min
            total_obj_size = sum(
                _get_bounds_on_axis(o, axis_idx)[1] - _get_bounds_on_axis(o, axis_idx)[0]
                for o in objects
            )

            available_gap = total_span - total_obj_size
            gap = available_gap / (len(objects) - 1) if len(objects) > 1 else 0

            # Position each object after the first
            current_pos = first_max + gap
            for obj in objects[1:-1]:
                obj_min, obj_max = _get_bounds_on_axis(obj, axis_idx)
                obj_size = obj_max - obj_min
                obj_center = obj.location[axis_idx]
                obj_offset = obj_center - obj_min

                obj.location[axis_idx] = current_pos + obj_offset
                current_pos += obj_size + gap

        self.report({'INFO'}, f"Distributed {len(objects)} objects along {self.axis}")
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_DistributeObjects,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
