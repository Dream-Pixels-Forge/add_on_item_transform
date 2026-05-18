"""
Item Transform Pro - Professional Transform Toolkit for Blender
===============================================================
A comprehensive transform addon providing quick transforms, alignment,
distribution, stacking, randomization, array placement, surface snapping,
transform presets, and utility operations.

Compatible with Blender 4.2+ / 5.x Extension System.
"""

import bpy

from . import i18n
from . import operators
from . import panels
from . import preferences
from . import properties
from . import pie_menu
from . import menus


# ============================================================
# Registration
# ============================================================

modules = (
    i18n,
    properties,
    preferences,
    operators,
    panels,
    menus,
    pie_menu,
)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
