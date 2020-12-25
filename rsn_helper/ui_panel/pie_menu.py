import bpy
from bpy.types import Menu
import rna_keymap_ui

class RSN_MT_PieMenu(Menu):
    bl_label = "RSN Helper"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("rsn.merge_task")
        pie.operator("rsn.simple_task")
        pie.operator("rsn.add_viewer_node")

addon_keymaps = []

def register():
    bpy.utils.register_class(RSN_MT_PieMenu)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # ssm pie menu
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS')
        kmi.properties.name = "RSN Helper"
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(RSN_MT_PieMenu)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()

