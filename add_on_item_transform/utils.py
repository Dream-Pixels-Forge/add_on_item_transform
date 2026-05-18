"""
Shared utility functions for Item Transform Pro.

Centralizes common operations like bounding-box calculations, axis mapping,
and object filtering to eliminate duplication across operator modules.
"""

from mathutils import Vector


# ============================================================
# Axis Helpers
# ============================================================

AXIS_INDEX = {'X': 0, 'Y': 1, 'Z': 2}

DIRECTION_VECTORS = {
    'X': Vector((1, 0, 0)),
    '-X': Vector((-1, 0, 0)),
    'Y': Vector((0, 1, 0)),
    '-Y': Vector((0, -1, 0)),
    'Z': Vector((0, 0, 1)),
    '-Z': Vector((0, 0, -1)),
    'POS_X': Vector((1, 0, 0)),
    'NEG_X': Vector((-1, 0, 0)),
    'POS_Y': Vector((0, 1, 0)),
    'NEG_Y': Vector((0, -1, 0)),
    'POS_Z': Vector((0, 0, 1)),
    'NEG_Z': Vector((0, 0, -1)),
}


def axis_index(axis_name):
    """
    Convert an axis name to its integer index.

    Args:
        axis_name: 'X', 'Y', 'Z', '-X', '-Y', or '-Z'

    Returns:
        int: 0, 1, or 2
    """
    return AXIS_INDEX.get(axis_name.lstrip('-'), 0)


def axis_sign(direction):
    """
    Determine the sign of a direction string.

    Args:
        direction: e.g. 'X', '-X', 'POS_X', 'NEG_X'

    Returns:
        int: 1 or -1
    """
    if direction.startswith('-') or direction.startswith('NEG'):
        return -1
    return 1


# ============================================================
# Bounding Box Functions
# ============================================================

def get_world_bounds(obj):
    """
    Get all 8 world-space bounding box corners of an object.

    Args:
        obj: A Blender object with a bound_box attribute.

    Returns:
        list[Vector]: 8 world-space corner positions.
        Returns [obj.location] as fallback for objects without bound_box.
    """
    if hasattr(obj, 'bound_box') and obj.bound_box:
        return [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    # Fallback for empties, cameras, lights, etc.
    return [obj.matrix_world.translation.copy()]


def get_bounds_on_axis(obj, axis_idx):
    """
    Get the minimum and maximum extent of an object on a specific axis.

    Args:
        obj: A Blender object.
        axis_idx: 0 (X), 1 (Y), or 2 (Z).

    Returns:
        tuple[float, float]: (min_value, max_value) on that axis.
    """
    bounds = get_world_bounds(obj)
    values = [v[axis_idx] for v in bounds]
    return min(values), max(values)


def get_bounds_center(obj):
    """
    Get the world-space center of an object's bounding box.

    Returns:
        Vector: Center point of the bounding box.
    """
    bounds = get_world_bounds(obj)
    return sum(bounds, Vector((0, 0, 0))) / len(bounds)


def get_bounds_size(obj):
    """
    Get the world-space dimensions (size) of an object's bounding box.

    Returns:
        Vector: (width_x, width_y, width_z)
    """
    bounds = get_world_bounds(obj)
    xs = [v.x for v in bounds]
    ys = [v.y for v in bounds]
    zs = [v.z for v in bounds]
    return Vector((max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)))


def get_bounds_min(obj):
    """
    Get the world-space minimum corner of the bounding box.

    Returns:
        Vector: (min_x, min_y, min_z)
    """
    bounds = get_world_bounds(obj)
    return Vector((
        min(v.x for v in bounds),
        min(v.y for v in bounds),
        min(v.z for v in bounds),
    ))


def get_bounds_max(obj):
    """
    Get the world-space maximum corner of the bounding box.

    Returns:
        Vector: (max_x, max_y, max_z)
    """
    bounds = get_world_bounds(obj)
    return Vector((
        max(v.x for v in bounds),
        max(v.y for v in bounds),
        max(v.z for v in bounds),
    ))


def get_bound_value(obj, axis_idx, mode):
    """
    Get a specific alignment reference value for an object.

    Args:
        obj: A Blender object.
        axis_idx: 0, 1, or 2.
        mode: 'MIN', 'MAX', or 'CENTER'.

    Returns:
        float: The reference value on the specified axis.
    """
    bounds = get_world_bounds(obj)
    values = [v[axis_idx] for v in bounds]

    if mode == 'MIN':
        return min(values)
    elif mode == 'MAX':
        return max(values)
    else:  # CENTER
        return (min(values) + max(values)) / 2.0


# ============================================================
# Object Filtering
# ============================================================

def filter_mesh_objects(objects):
    """
    Filter a list of objects to include only mesh-like objects
    (those with bound_box data).

    Args:
        objects: Iterable of Blender objects.

    Returns:
        list: Filtered objects that have valid bounding boxes.
    """
    return [obj for obj in objects if hasattr(obj, 'bound_box') and obj.bound_box]


def get_collection_for_object(obj, fallback_collection=None):
    """
    Get the first collection an object belongs to.

    Args:
        obj: A Blender object.
        fallback_collection: Collection to return if object has no collections.

    Returns:
        bpy.types.Collection or None
    """
    if obj.users_collection:
        return obj.users_collection[0]
    return fallback_collection
