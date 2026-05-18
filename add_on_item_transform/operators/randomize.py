"""
Randomize operators - Add random offsets to object transforms.
"""

import math
import random

import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
)


class OBJECT_OT_RandomizeTransform(bpy.types.Operator):
    """Randomize transforms of selected objects"""

    bl_idname = "object.item_transform_randomize"
    bl_label = "Randomize Transform"
    bl_options = {'REGISTER', 'UNDO'}

    seed: IntProperty(
        name="Seed",
        description="Random seed (0 = use current time)",
        default=0,
        min=0,
    )

    use_location: BoolProperty(name="Location", default=True)
    use_rotation: BoolProperty(name="Rotation", default=False)
    use_scale: BoolProperty(name="Scale", default=False)

    loc_range: FloatVectorProperty(
        name="Location Range",
        description="Maximum random offset per axis",
        size=3,
        default=(1.0, 1.0, 1.0),
        min=0.0,
        subtype='TRANSLATION',
    )

    rot_range: FloatVectorProperty(
        name="Rotation Range",
        description="Maximum random rotation per axis (radians)",
        size=3,
        default=(0.0, 0.0, math.pi),
        min=0.0,
        subtype='EULER',
    )

    scale_uniform: BoolProperty(
        name="Uniform Scale",
        description="Same scale on all axes",
        default=True,
    )

    scale_min: FloatProperty(
        name="Scale Min",
        default=0.8,
        min=0.001,
    )

    scale_max: FloatProperty(
        name="Scale Max",
        default=1.2,
        min=0.001,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def invoke(self, context, event):
        # Pre-fill from scene properties
        props = context.scene.item_transform
        self.seed = props.random_seed
        self.use_location = props.use_location
        self.use_rotation = props.use_rotation
        self.use_scale = props.use_scale
        self.loc_range = props.random_location
        self.rot_range = props.random_rotation
        self.scale_uniform = props.random_scale_uniform
        self.scale_min = props.random_scale_range[0]
        self.scale_max = props.random_scale_range[1]
        return self.execute(context)

    def execute(self, context):
        objects = context.selected_objects

        rng = random.Random(self.seed if self.seed != 0 else None)

        for obj in objects:
            if self.use_location:
                for i in range(3):
                    obj.location[i] += rng.uniform(-self.loc_range[i], self.loc_range[i])

            if self.use_rotation:
                for i in range(3):
                    obj.rotation_euler[i] += rng.uniform(-self.rot_range[i], self.rot_range[i])

            if self.use_scale:
                if self.scale_uniform:
                    s = rng.uniform(self.scale_min, self.scale_max)
                    obj.scale *= s
                else:
                    for i in range(3):
                        obj.scale[i] *= rng.uniform(self.scale_min, self.scale_max)

        self.report(
            {'INFO'},
            f"Randomized {len(objects)} object(s)",
        )
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_RandomizeTransform,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
