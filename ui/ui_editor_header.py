import bpy
from ..preferences import get_pref, RSN_Preference
from .icon_utils import RSN_Preview

rsn_icon = RSN_Preview(image='rsn.bip', name='rsn_icon')


def draw_swith_tree(self, context):
    layout = self.layout
    layout.separator()
    layout.operator('rsn.switch_to_bind_tree', icon_value=rsn_icon.get_image_icon_id())


def draw_overlay(self, context):
    if context.area.ui_type == 'RenderNodeTree' and context.space_data.node_tree is not None:
        layout = self.layout
        layout.separator(factor=0.5)

        pref = get_pref()

        box = layout.box().column(align=1)
        if context.scene.RSNBusyDrawing is True:
            box.prop(context.scene, 'RSNBusyDrawing', text='Drawing...', toggle=1, icon='SORTTIME')
        else:
            box.operator("rsn.draw_nodes", icon='TIME')

        box.separator(factor=1)

        box.prop(pref.draw_nodes, 'size', slider=True)
        box.label(text='Time Color')
        row = box.row()
        row.prop(pref.draw_nodes, 'text_color1', text='')
        row.prop(pref.draw_nodes, 'text_color2', text='')
        row.prop(pref.draw_nodes, 'text_color3', text='')


def register():
    rsn_icon.register()

    bpy.types.NODE_MT_editor_menus.append(draw_swith_tree)
    if bpy.app.version > (2, 9, 3):
        bpy.types.NODE_PT_overlay.append(draw_overlay)


def unregister():
    rsn_icon.unregister()

    bpy.types.NODE_MT_editor_menus.remove(draw_swith_tree)
    if bpy.app.version > (2, 9, 3):
        bpy.types.NODE_PT_overlay.remove(draw_overlay)
