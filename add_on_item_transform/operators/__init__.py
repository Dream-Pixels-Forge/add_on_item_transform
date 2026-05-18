"""
Operators package - All operators for Item Transform Pro.
"""

from . import quick_transform
from . import align
from . import distribute
from . import stack
from . import randomize
from . import utilities
from . import pivot


modules = (
    quick_transform,
    align,
    distribute,
    stack,
    randomize,
    utilities,
    pivot,
)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
