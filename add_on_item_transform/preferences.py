"""
Preferences module - Addon preferences accessible from Edit > Preferences > Add-ons.
"""

import bpy
from bpy.props import EnumProperty, StringProperty


class ITEM_TRANSFORM_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    pie_menu_key: EnumProperty(
        name="Pie Menu Key",
        description="Key to open the Item Transform pie menu",
        items=[
            ('T', "T", ""),
            ('Q', "Q", ""),
            ('D', "D", ""),
            ('W', "W", ""),
        ],
        default='T',
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
        row = box.row()
        row.prop(self, "pie_menu_key")
        row.label(text="(Shift + Alt + Key)")

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
