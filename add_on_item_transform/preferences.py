"""
Preferences module - Addon preferences accessible from Edit > Preferences > Add-ons.
Supports live keymap updates without requiring a Blender restart.
"""

import bpy
from bpy.props import EnumProperty


def _update_pie_menu_key(self, context):
    """Callback: re-register the pie menu keymap when preference changes."""
    from . import pie_menu
    pie_menu.refresh_keymap()


class ITEM_TRANSFORM_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    pie_menu_key: EnumProperty(
        name="Pie Menu Key",
        description="Key to open the Item Transform pie menu (Shift+Alt+Key)",
        items=[
            ('T', "T", "Shift+Alt+T"),
            ('Q', "Q", "Shift+Alt+Q"),
            ('D', "D", "Shift+Alt+D"),
            ('W', "W", "Shift+Alt+W"),
            ('E', "E", "Shift+Alt+E"),
            ('X', "X", "Shift+Alt+X"),
        ],
        default='T',
        update=_update_pie_menu_key,
    )

    default_panel_location: EnumProperty(
        name="Panel Location",
        description="Where to display the main panel",
        items=[
            ('PROPERTIES', "Properties Editor", "Show in Properties > Object"),
            ('VIEW_3D', "3D Viewport Sidebar", "Show in N-Panel (sidebar)"),
            ('BOTH', "Both", "Show in both locations"),
        ],
        default='BOTH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Item Transform Pro Preferences", icon='PREFERENCES')

        box = layout.box()
        box.label(text="Keyboard Shortcuts:", icon='EVENT_OS')
        col = box.column(align=True)
        row = col.row()
        row.prop(self, "pie_menu_key")
        row.label(text="(Shift + Alt + Key)")
        col.label(
            text="Keymap updates live — no restart needed.",
            icon='CHECKMARK',
        )

        box = layout.box()
        box.label(text="Panel Location:", icon='WINDOW')
        box.prop(self, "default_panel_location", text="")
        box.label(
            text="Note: Restart Blender or disable/enable addon to apply panel changes.",
            icon='INFO',
        )


# ============================================================
# Registration
# ============================================================

classes = (
    ITEM_TRANSFORM_Preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
