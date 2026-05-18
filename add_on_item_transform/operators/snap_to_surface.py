"""
Snap to Surface operators - Project objects onto the surface of other objects
using raycasting. Supports snapping to ground plane, active object surface,
or nearest surface in the scene.
"""

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from mathutils import Vector


def _raycast_scene(context, origin, direction, exclude_objects=None):
    """
    Cast a ray into the scene depsgraph and return the hit result.

    Returns:
        tuple: (hit, location, normal, face_index, object, matrix)
               or None if no hit.
    """
    depsgraph = context.evaluated_depsgraph_get()
    exclude = set(exclude_objects or [])

    result = context.scene.ray_cast(depsgraph, origin, direction)
    # result = (success, location, normal, index, object, matrix)

    if result[0] and result[4] not in exclude:
        return result
    return None


def _get_object_bottom(obj):
    """Get the lowest point of an object in world space."""
    bounds = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return min(v.z for v in bounds)


def _get_object_center_bottom(obj):
    """Get the XY center and Z bottom of an object's bounding box in world space."""
    bounds = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    center_x = sum(v.x for v in bounds) / 8.0
    center_y = sum(v.y for v in bounds) / 8.0
    bottom_z = min(v.z for v in bounds)
    return Vector((center_x, center_y, bottom_z))


class OBJECT_OT_SnapToSurface(bpy.types.Operator):
    """Snap selected objects onto the surface below them (raycast downward)"""

    bl_idname = "object.item_transform_snap_to_surface"
    bl_label = "Snap to Surface"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        description="Direction to cast the ray",
        items=[
            ('DOWN', "Down (-Z)", "Cast ray downward"),
            ('UP', "Up (+Z)", "Cast ray upward"),
            ('FORWARD', "Forward (-Y)", "Cast ray forward"),
            ('BACK', "Back (+Y)", "Cast ray backward"),
            ('LEFT', "Left (-X)", "Cast ray to the left"),
            ('RIGHT', "Right (+X)", "Cast ray to the right"),
        ],
        default='DOWN',
    )

    align_to_normal: BoolProperty(
        name="Align to Normal",
        description="Rotate object to align with the surface normal",
        default=False,
    )

    offset: FloatProperty(
        name="Offset",
        description="Distance offset from the surface",
        default=0.0,
        soft_min=-10.0,
        soft_max=10.0,
        subtype='DISTANCE',
    )

    use_bottom: BoolProperty(
        name="Use Bottom",
        description="Place the object's bottom on the surface (instead of origin)",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        direction_map = {
            'DOWN': Vector((0, 0, -1)),
            'UP': Vector((0, 0, 1)),
            'FORWARD': Vector((0, -1, 0)),
            'BACK': Vector((0, 1, 0)),
            'LEFT': Vector((-1, 0, 0)),
            'RIGHT': Vector((1, 0, 0)),
        }

        ray_dir = direction_map[self.direction]
        snapped = 0

        for obj in context.selected_objects:
            # Use center-bottom or origin as ray origin
            if self.use_bottom:
                ray_origin = _get_object_center_bottom(obj)
            else:
                ray_origin = obj.location.copy()

            # Offset ray origin slightly against the direction to avoid self-intersection
            ray_origin -= ray_dir * 0.001

            # Perform raycast excluding the object itself
            result = _raycast_scene(context, ray_origin, ray_dir, exclude_objects=[obj])

            if result is None:
                continue

            _success, hit_location, hit_normal, _index, _hit_obj, _matrix = result

            # Calculate the offset between object origin and bottom
            if self.use_bottom:
                bottom_offset = obj.location.z - _get_object_bottom(obj)
            else:
                bottom_offset = 0.0

            # Determine the primary axis index for the direction
            axis_map = {
                'DOWN': 2, 'UP': 2,
                'FORWARD': 1, 'BACK': 1,
                'LEFT': 0, 'RIGHT': 0,
            }
            axis_idx = axis_map[self.direction]

            # Position the object at the hit point
            if self.direction in ('DOWN', 'UP'):
                obj.location.z = hit_location.z + bottom_offset + self.offset
            elif self.direction in ('FORWARD', 'BACK'):
                obj.location.y = hit_location.y + self.offset
            else:
                obj.location.x = hit_location.x + self.offset

            # Optionally align to surface normal
            if self.align_to_normal:
                # Use track-to to align Z-up to the surface normal
                obj.rotation_euler = hit_normal.to_track_quat('Z', 'Y').to_euler()

            snapped += 1

        if snapped == 0:
            self.report({'WARNING'}, "No surfaces found below selected objects")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Snapped {snapped} object(s) to surface")
        return {'FINISHED'}


class OBJECT_OT_SnapToActive(bpy.types.Operator):
    """Snap selected objects onto the surface of the active object"""

    bl_idname = "object.item_transform_snap_to_active"
    bl_label = "Snap to Active Surface"
    bl_options = {'REGISTER', 'UNDO'}

    align_to_normal: BoolProperty(
        name="Align to Normal",
        description="Rotate object to align with the hit surface normal",
        default=False,
    )

    offset: FloatProperty(
        name="Offset",
        description="Distance offset from the active object's surface",
        default=0.0,
        soft_min=-10.0,
        soft_max=10.0,
        subtype='DISTANCE',
    )

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and len(context.selected_objects) >= 2
            and context.mode == 'OBJECT'
        )

    def execute(self, context):
        active = context.active_object
        targets = [o for o in context.selected_objects if o != active]

        if not targets:
            self.report({'WARNING'}, "No objects to snap (active is excluded)")
            return {'CANCELLED'}

        snapped = 0
        depsgraph = context.evaluated_depsgraph_get()

        # Get evaluated version of the active object for raycasting
        active_eval = active.evaluated_get(depsgraph)

        for obj in targets:
            # Cast a ray from the object toward the active object's center
            direction = (active.location - obj.location).normalized()
            ray_origin = obj.location.copy()

            # Use scene raycast but we check if we hit the active
            result = context.scene.ray_cast(depsgraph, ray_origin, direction)

            if result[0] and result[4] == active_eval:
                hit_location = result[1]
                hit_normal = result[2]

                # Place on surface with offset along the normal
                obj.location = hit_location + hit_normal * self.offset

                if self.align_to_normal:
                    obj.rotation_euler = hit_normal.to_track_quat('Z', 'Y').to_euler()

                snapped += 1

        if snapped == 0:
            self.report({'WARNING'}, "Could not snap objects to active surface")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Snapped {snapped} object(s) to active surface")
        return {'FINISHED'}


class OBJECT_OT_DropToGround(bpy.types.Operator):
    """Drop objects to the ground plane or nearest surface below using raycast"""

    bl_idname = "object.item_transform_drop_to_ground"
    bl_label = "Drop to Ground"
    bl_options = {'REGISTER', 'UNDO'}

    use_scene_geometry: BoolProperty(
        name="Use Scene Geometry",
        description="Drop onto scene geometry (not just Z=0 plane)",
        default=True,
    )

    offset: FloatProperty(
        name="Offset",
        description="Height offset from the landing surface",
        default=0.0,
        soft_min=-5.0,
        soft_max=5.0,
        subtype='DISTANCE',
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):
        dropped = 0

        for obj in context.selected_objects:
            bottom_z = _get_object_bottom(obj)
            origin_to_bottom = obj.location.z - bottom_z

            if self.use_scene_geometry:
                # Raycast downward from object center
                ray_origin = obj.location.copy()
                ray_origin.z = obj.location.z + 0.001  # Slight offset up

                result = _raycast_scene(
                    context, ray_origin, Vector((0, 0, -1)), exclude_objects=[obj]
                )

                if result:
                    hit_z = result[1].z
                    obj.location.z = hit_z + origin_to_bottom + self.offset
                    dropped += 1
                else:
                    # Fallback to Z=0
                    obj.location.z = origin_to_bottom + self.offset
                    dropped += 1
            else:
                # Simple Z=0 ground plane
                obj.location.z = origin_to_bottom + self.offset
                dropped += 1

        self.report({'INFO'}, f"Dropped {dropped} object(s) to ground")
        return {'FINISHED'}


# ============================================================
# Registration
# ============================================================

classes = (
    OBJECT_OT_SnapToSurface,
    OBJECT_OT_SnapToActive,
    OBJECT_OT_DropToGround,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
