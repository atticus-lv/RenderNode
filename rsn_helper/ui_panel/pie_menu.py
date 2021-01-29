import bpy
from bpy.types import Menu
from bpy.props import *
import rna_keymap_ui


class RSN_OT_SwitchTree(bpy.types.Operator):
    bl_idname = "rsn.switch_tree"
    bl_label = 'Switch Tree'

    tree_name: StringProperty()

    def execute(self, context):
        try:
            context.space_data.node_tree = bpy.data.node_groups[self.tree_name]
        except Exception as e:
            print(e)

        return {'FINISHED'}


class RSN_MT_PieMenu(Menu):
    bl_label = "RSN Helper"
    bl_idname = "RSN_MT_PieMenu"

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.25
        pie = layout.menu_pie()

        # left
        pie.separator()

        # right
        col1 = pie.column()
        col = col1.box().column()
        col.operator("rsn.move_node", text='Simple Task')

        col = col1.box().column()
        col.operator("rsn.merge_selected_nodes", icon='OUTLINER')

        # bottom
        if context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree':
            col = pie.column(align=1)
            box = col.box()

            for g in bpy.data.node_groups:
                if g.bl_idname == 'RenderStackNodeTree':
                    row = box.row(align=1)
                    row.prop(bpy.data.node_groups[g.name], 'name', text='')
                    row.prop(bpy.data.node_groups[g.name], 'use_fake_user', icon_only=1)
                    if context.space_data.edit_tree != bpy.data.node_groups[g.name]:
                        row.operator('rsn.switch_tree', icon='SCREEN_BACK', text='').tree_name = g.name
                    else:
                        row.label(icon='HIDE_OFF', text='')

            box.operator("node.new_node_tree", text='New Tree', icon='ADD')
        else:
            pie.operator("node.new_node_tree")


addon_keymaps = []


def register():
    bpy.utils.register_class(RSN_MT_PieMenu)
    bpy.utils.register_class(RSN_OT_SwitchTree)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # ssm pie menu
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS')
        kmi.properties.name = "RSN_MT_PieMenu"
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(RSN_MT_PieMenu)
    bpy.utils.unregister_class(RSN_OT_SwitchTree)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()
