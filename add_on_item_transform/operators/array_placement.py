"""
Array Placement operators - Create copies of objects in circular, grid,
or linear patterns. Non-destructive duplication with precise control.
"""

import math

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
)
from mathutils import Matrix, Vector


class OBJECT_OT_CircularArray(bpy.types.Operator):
    """Duplicate selected objects in a circular (radial) pattern"""

    bl_idname = "object.item_transform_circular_array"
    bl_label = "Circular Array"
    bl_options = {'REGISTER', 'UNDO'}

    count: IntProperty(
        name="Count",
        description="Number of copies (including original)",
        default=6,
        min=2,
        max=360,
    )

    radius: FloatProperty(
        name="Radius",
        description="Radius of the circle",
        default=3.0,
        min=0.001,
        soft_max=100.0,
        subtype='DISTANCE',
    )

    axis: EnumProperty(
        name="Axis",
        description="Axis of revolution",
        items=[
            ('X', "X", "Revolve around X axis"),
            ('Y', "Y", "Revolve around Y axis"),
            ('Z', "Z", "Revolve around Z axis"),
        ],
        default='Z',
    )

    start_angle: FloatProperty(
        name="Start Angle",
        description="Starting angle offset",
        default=0.0,
        subtype='ANGLE',
        unit='ROTATION',
    )

    end_angle: FloatProperty(
        name="End Angle",
        description="End angle (360 = full circle)",
        default=math.radians(360.0),
        subtype='ANGLE',
        unit='ROTATION',
    )

    rotate_copies: BoolProperty(
        name="Rotate Copies",
        description="Rotate each copy to face outward from center",
        default=True,
    )

    use_linked: BoolProperty(
        name="Linked Duplicates",
        description="Create linked (instanced) duplicates instead of full copies",
        default=False,
    )

    center: FloatVectorProperty(
        name="Center",
        description="Center point of the circular array",
        size=3,
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        original_objects = list(context.selected_objects)
        created = []

        # Full circle vs arc
        full_circle = abs(self.end_angle - self.start_angle - math.radians(360.0)) < 0.001
        if full_circle:
            angle_step = (self.end_angle - self.start_angle) / self.count
        else:
            angle_step = (self.end_angle - self.start_angle) / max(1, self.count - 1)

        center = Vector(self.center)

        for obj in original_objects:
            for i in range(self.count):
                angle = self.start_angle + angle_step * i

                # Calculate position on the circle
                if self.axis == 'Z':
                    offset = Vector((
                        math.cos(angle) * self.radius,
                        math.sin(angle) * self.radius,
                        0.0,
                    ))
                elif self.axis == 'X':
                    offset = Vector((
                        0.0,
                        math.cos(angle) * self.radius,
                        math.sin(angle) * self.radius,
                    ))
                else:  # Y
                    offset = Vector((
                        math.cos(angle) * self.radius,
                        0.0,
                        math.sin(angle) * self.radius,
                    ))

                # Skip the first copy if it's the original position
                if i == 0:
                    # Move original to first position
                    obj.location = center + offset
                    if self.rotate_copies:
                        if self.axis == 'Z':
                            obj.rotation_euler.z = angle
                        elif self.axis == 'X':
                            obj.rotation_euler.x = angle
                        else:
                            obj.rotation_euler.y = angle
                    continue

                # Duplicate
                new_obj = obj.copy()
                if not self.use_linked and obj.data:
                    new_obj.data = obj.data.copy()

                new_obj.location = center + offset

                if self.rotate_copies:
                    if self.axis == 'Z':
                        new_obj.rotation_euler.z = angle
                    elif self.axis == 'X':
                        new_obj.rotation_euler.x = angle
                    else:
                        new_obj.rotation_euler.y = angle

                # Link to same collection as original
                for coll in obj.users_collection:
                    coll.objects.link(new_obj)
                    break
                else:
                    context.collection.objects.link(new_obj)

                created.append(new_obj)

        # Select all created objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in created + original_objects:
            obj.select_set(True)

        self.report(
            {'INFO'},
            f"Created circular array: {len(created)} new copies "
            f"(radius={self.radius:.2f}, axis={self.axis})",
        )
        return {'FINISHED'}


class OBJECT_OT_GridArray(bpy.types.Operator):
    """Duplicate selected objects in a grid (rows x columns) pattern"""

    bl_idname = "object.item_transform_grid_array"
    bl_label = "Grid Array"
    bl_options = {'REGISTER', 'UNDO'}

    rows: IntProperty(
        name="Rows",
        description="Number of rows",
        default=3,
        min=1,
        max=100,
    )

    columns: IntProperty(
        name="Columns",
        description="Number of columns",
        default=3,
        min=1,
        max=100,
    )

    layers: IntProperty(
        name="Layers",
        description="Number of vertical layers (Z)",
        default=1,
        min=1,
        max=50,
    )

    spacing_x: FloatProperty(
        name="Spacing X",
        description="Distance between columns",
        default=2.0,
        min=0.0,
        soft_max=50.0,
        subtype='DISTANCE',
    )

    spacing_y: FloatProperty(
        name="Spacing Y",
        description="Distance between rows",
        default=2.0,
        min=0.0,
        soft_max=50.0,
        subtype='DISTANCE',
    )

    spacing_z: FloatProperty(
        name="Spacing Z",
        description="Distance between layers",
        default=2.0,
        min=0.0,
        soft_max=50.0,
        subtype='DISTANCE',
    )

    center_grid: BoolProperty(
        name="Center Grid",
        description="Center the grid around the original object's position",
        default=True,
    )

    use_linked: BoolProperty(
        name="Linked Duplicates",
        description="Create linked (instanced) duplicates",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        original_objects = list(context.selected_objects)
        created = []

        for obj in original_objects:
            base_loc = obj.location.copy()

            # Calculate centering offset
            if self.center_grid:
                offset_x = (self.columns - 1) * self.spacing_x / 2.0
                offset_y = (self.rows - 1) * self.spacing_y / 2.0
                offset_z = (self.layers - 1) * self.spacing_z / 2.0
            else:
                offset_x = offset_y = offset_z = 0.0

            first = True
            for z in range(self.layers):
                for row in range(self.rows):
                    for col in range(self.columns):
                        pos = Vector((
                            base_loc.x + col * self.spacing_x - offset_x,
                            base_loc.y + row * self.spacing_y - offset_y,
                            base_loc.z + z * self.spacing_z - offset_z,
                        ))

                        if first:
                            # Place original at first position
                            obj.location = pos
                            first = False
                            continue

                        # Duplicate
                        new_obj = obj.copy()
                        if not self.use_linked and obj.data:
                            new_obj.data = obj.data.copy()

                        new_obj.location = pos

                        for coll in obj.users_collection:
                            coll.objects.link(new_obj)
                            break
                        else:
                            context.collection.objects.link(new_obj)

                        created.append(new_obj)

        # Select all
        bpy.ops.object.select_all(action='DESELECT')
        for obj in created + original_objects:
            obj.select_set(True)

        total = self.rows * self.columns * self.layers
        self.report(
            {'INFO'},
            f"Created {total}-element grid ({self.columns}x{self.rows}x{self.layers}), "
            f"{len(created)} new copies",
        )
        return {'FINISHED'}


class OBJECT_OT_LinearArray(bpy.types.Operator):
    """Duplicate selected objects in a linear pattern along a direction"""

    bl_idname = "object.item_transform_linear_array"
    bl_label = "Linear Array"
    bl_options = {'REGISTER', 'UNDO'}

    count: IntProperty(
        name="Count",
        description="Number of copies (including original)",
        default=5,
        min=2,
        max=500,
    )

    offset: FloatVectorProperty(
        name="Offset",
        description="Offset vector between each copy",
        size=3,
        default=(2.0, 0.0, 0.0),
        subtype='TRANSLATION',
    )

    use_progressive_rotation: BoolProperty(
        name="Progressive Rotation",
        description="Add incremental rotation to each copy",
        default=False,
    )

    rotation_step: FloatVectorProperty(
        name="Rotation Step",
        description="Incremental rotation per copy",
        size=3,
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
    )

    use_progressive_scale: BoolProperty(
        name="Progressive Scale",
        description="Add incremental scale to each copy",
        default=False,
    )

    scale_step: FloatProperty(
        name="Scale Step",
        description="Scale multiplier per step (1.0 = no change)",
        default=1.0,
        min=0.01,
        soft_max=2.0,
    )

    use_linked: BoolProperty(
        name="Linked Duplicates",
        description="Create linked (instanced) duplicates",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        original_objects = list(context.selected_objects)
        offset_vec = Vector(self.offset)
        created = []

        for obj in original_objects:
            base_loc = obj.location.copy()
            base_rot = obj.rotation_euler.copy()
            base_scale = obj.scale.copy()

            for i in range(1, self.count):
                # Duplicate
                new_obj = obj.copy()
                if not self.use_linked and obj.data:
                    new_obj.data = obj.data.copy()

                # Position
                new_obj.location = base_loc + offset_vec * i

                # Progressive rotation
                if self.use_progressive_rotation:
                    new_obj.rotation_euler.x = base_rot.x + self.rotation_step[0] * i
                    new_obj.rotation_euler.y = base_rot.y + self.rotation_step[1] * i
                    new_obj.rotation_euler.z = base_rot.z + self.rotation_step[2] * i

                # Progressive scale
                if self.use_progressive_scale:
                    scale_factor = self.scale_step ** i
                    new_obj.scale = base_scale * scale_factor

                # Link to collection
                for coll in obj.users_collection:
                    coll.objects.link(new_obj)
                    break
                else:
                    context.collection.objects.link(new_obj)

                created.append(new_obj)

        # Select all
        bpy.ops.object.select_all(action='DESELECT')
        for obj in created + original_objects:
            obj.select_set(True)

        self.report(
            {'INFO'},
            f"Created linear array: {len(created)} new copies "
            f"(offset={tuple(round(v, 2) for v in self.offset)})",
        )
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_CircularArray,
    OBJECT_OT_GridArray,
    OBJECT_OT_LinearArray,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
