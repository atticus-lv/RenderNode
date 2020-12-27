import bpy
from bpy.types import Menu
import rna_keymap_ui


class RSN_MT_PieMenu(Menu):
    bl_label = "RSN Helper"
    bl_idname = "RSN_MT_PieMenu"

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.25

        pie = layout.menu_pie()
        col = pie.box().column()
        col.operator("rsn.move_node", text='Simple Task')
        col.operator("rsn.add_viewer_node", icon='HIDE_OFF', text='View Task')

        col = pie.box().column()
        col.operator("rsn.merge_settings", icon='OUTLINER')
        col.operator("rsn.merge_task", icon='OUTLINER')

        # pie.operator('node.add_search')

        if context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree':
            row = pie.box().row(align=True)
            row.prop(context.space_data.edit_tree, 'name')
            row.prop(context.space_data.edit_tree, 'use_fake_user', icon_only=1)


addon_keymaps = []


def register():
    bpy.utils.register_class(RSN_MT_PieMenu)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # ssm pie menu
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS')
        kmi.properties.name = "RSN_MT_PieMenu"
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(RSN_MT_PieMenu)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()
