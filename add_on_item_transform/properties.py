"""
Properties module - Defines all addon property groups.
"""

import bpy
from bpy.props import (
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    BoolProperty,
    IntProperty,
)


class ITEM_TRANSFORM_Properties(bpy.types.PropertyGroup):
    """Main property group for Item Transform Pro."""

    # --- Transform Factors ---
    move_factor: FloatProperty(
        name="Move Factor",
        description="Distance to move per step (in scene units)",
        default=1.0,
        min=0.001,
        soft_max=100.0,
        step=10,
        precision=3,
        subtype='DISTANCE',
    )

    rotate_factor: FloatProperty(
        name="Rotate Factor",
        description="Angle to rotate per step",
        default=15.0,
        min=0.01,
        soft_max=180.0,
        step=100,
        precision=2,
        subtype='ANGLE',
        unit='ROTATION',
    )

    scale_factor: FloatProperty(
        name="Scale Factor",
        description="Percentage to scale per step",
        default=10.0,
        min=0.1,
        soft_max=200.0,
        step=100,
        precision=1,
        subtype='PERCENTAGE',
    )

    # --- Stack Direction ---
    stack_direction: EnumProperty(
        name="Stack Direction",
        description="Axis along which to stack objects",
        items=[
            ('X', "+X", "Stack along positive X axis", 'AXIS_SIDE', 0),
            ('-X', "-X", "Stack along negative X axis", 'AXIS_SIDE', 1),
            ('Y', "+Y", "Stack along positive Y axis", 'AXIS_FRONT', 2),
            ('-Y', "-Y", "Stack along negative Y axis", 'AXIS_FRONT', 3),
            ('Z', "+Z", "Stack along positive Z axis", 'AXIS_TOP', 4),
            ('-Z', "-Z", "Stack along negative Z axis", 'AXIS_TOP', 5),
        ],
        default='Z',
    )

    stack_gap: FloatProperty(
        name="Gap",
        description="Gap between stacked objects",
        default=0.0,
        soft_min=-10.0,
        soft_max=10.0,
        step=10,
        precision=3,
        subtype='DISTANCE',
    )

    # --- Align Settings ---
    align_axis: EnumProperty(
        name="Align Axis",
        description="Axis to align on",
        items=[
            ('X', "X", "Align on X axis"),
            ('Y', "Y", "Align on Y axis"),
            ('Z', "Z", "Align on Z axis"),
        ],
        default='X',
    )

    align_mode: EnumProperty(
        name="Align Mode",
        description="How to align objects",
        items=[
            ('MIN', "Min", "Align to minimum bound"),
            ('CENTER', "Center", "Align to center"),
            ('MAX', "Max", "Align to maximum bound"),
            ('CURSOR', "Cursor", "Align to 3D cursor"),
            ('ACTIVE', "Active", "Align to active object"),
        ],
        default='CENTER',
    )

    # --- Distribute Settings ---
    distribute_axis: EnumProperty(
        name="Distribute Axis",
        description="Axis to distribute along",
        items=[
            ('X', "X", "Distribute along X"),
            ('Y', "Y", "Distribute along Y"),
            ('Z', "Z", "Distribute along Z"),
        ],
        default='X',
    )

    distribute_mode: EnumProperty(
        name="Distribute Mode",
        description="How to distribute objects",
        items=[
            ('EVEN', "Even Spacing", "Equal gaps between objects"),
            ('CENTERS', "Even Centers", "Equal distance between centers"),
        ],
        default='EVEN',
    )

    # --- Randomize Settings ---
    random_seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0,
    )

    random_location: FloatVectorProperty(
        name="Location Range",
        description="Maximum random offset for each axis",
        size=3,
        default=(1.0, 1.0, 1.0),
        min=0.0,
        soft_max=100.0,
        subtype='TRANSLATION',
    )

    random_rotation: FloatVectorProperty(
        name="Rotation Range",
        description="Maximum random rotation for each axis (degrees)",
        size=3,
        default=(0.0, 0.0, 180.0),
        min=0.0,
        max=180.0,
        subtype='EULER',
    )

    random_scale_uniform: BoolProperty(
        name="Uniform Scale",
        description="Apply same random scale to all axes",
        default=True,
    )

    random_scale_range: FloatVectorProperty(
        name="Scale Range",
        description="Min/Max scale factor",
        size=2,
        default=(0.8, 1.2),
        min=0.01,
        soft_max=10.0,
    )

    # --- Flags ---
    use_location: BoolProperty(
        name="Location",
        description="Randomize location",
        default=True,
    )

    use_rotation: BoolProperty(
        name="Rotation",
        description="Randomize rotation",
        default=False,
    )

    use_scale: BoolProperty(
        name="Scale",
        description="Randomize scale",
        default=False,
    )


# ============================================================
# Registration
# ============================================================

classes = (
    ITEM_TRANSFORM_Properties,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.item_transform = bpy.props.PointerProperty(
        type=ITEM_TRANSFORM_Properties
    )


def unregister():
    del bpy.types.Scene.item_transform
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
