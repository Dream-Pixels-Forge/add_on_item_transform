"""
Quick Transform operators - Move, Rotate, Scale with configurable factors.
"""

import math

import bpy
from bpy.props import EnumProperty


class OBJECT_OT_QuickMove(bpy.types.Operator):
    """Move selected objects by the configured move factor"""

    bl_idname = "object.item_transform_quick_move"
    bl_label = "Quick Move"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        items=[
            ('POS_X', "+X", "Move along positive X"),
            ('NEG_X', "-X", "Move along negative X"),
            ('POS_Y', "+Y", "Move along positive Y"),
            ('NEG_Y', "-Y", "Move along negative Y"),
            ('POS_Z', "+Z", "Move along positive Z"),
            ('NEG_Z', "-Z", "Move along negative Z"),
        ],
        default='POS_X',
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        props = context.scene.item_transform
        factor = props.move_factor

        axis_map = {
            'POS_X': (0, 1),
            'NEG_X': (0, -1),
            'POS_Y': (1, 1),
            'NEG_Y': (1, -1),
            'POS_Z': (2, 1),
            'NEG_Z': (2, -1),
        }

        axis_idx, sign = axis_map[self.direction]

        for obj in context.selected_objects:
            obj.location[axis_idx] += factor * sign

        self.report({'INFO'}, f"Moved {len(context.selected_objects)} object(s) {self.direction}")
        return {'FINISHED'}


class OBJECT_OT_QuickRotate(bpy.types.Operator):
    """Rotate selected objects by the configured rotate factor"""

    bl_idname = "object.item_transform_quick_rotate"
    bl_label = "Quick Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "Rotate around X axis"),
            ('Y', "Y", "Rotate around Y axis"),
            ('Z', "Z", "Rotate around Z axis"),
        ],
        default='Z',
    )

    direction: EnumProperty(
        name="Direction",
        items=[
            ('POSITIVE', "+", "Positive rotation"),
            ('NEGATIVE', "-", "Negative rotation"),
        ],
        default='POSITIVE',
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        props = context.scene.item_transform
        # rotate_factor is already in radians due to subtype='ANGLE'
        angle = props.rotate_factor
        if self.direction == 'NEGATIVE':
            angle = -angle

        axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[self.axis]

        for obj in context.selected_objects:
            obj.rotation_euler[axis_idx] += angle

        deg = math.degrees(abs(angle))
        self.report(
            {'INFO'},
            f"Rotated {len(context.selected_objects)} object(s) "
            f"{deg:.1f}° around {self.axis}",
        )
        return {'FINISHED'}


class OBJECT_OT_QuickScale(bpy.types.Operator):
    """Scale selected objects by the configured scale factor"""

    bl_idname = "object.item_transform_quick_scale"
    bl_label = "Quick Scale"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        items=[
            ('UP', "Scale Up", "Increase scale"),
            ('DOWN', "Scale Down", "Decrease scale"),
        ],
        default='UP',
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        props = context.scene.item_transform
        factor = props.scale_factor / 100.0

        for obj in context.selected_objects:
            if self.direction == 'UP':
                obj.scale *= (1.0 + factor)
            else:
                new_scale = max(0.001, 1.0 - factor)
                obj.scale *= new_scale

        self.report(
            {'INFO'},
            f"Scaled {len(context.selected_objects)} object(s) "
            f"{'up' if self.direction == 'UP' else 'down'} by {props.scale_factor:.1f}%",
        )
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_QuickMove,
    OBJECT_OT_QuickRotate,
    OBJECT_OT_QuickScale,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
