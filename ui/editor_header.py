import bpy
from ..preferences import get_pref


def draw_item(self, context):
    if context.area.ui_type == 'RenderStackNodeTree' and context.space_data.node_tree is not None:
        layout = self.layout
        layout.separator(factor=0.5)
        row = layout.row(align=True)

        if context.scene.RSNBusyDrawing is True:
            row.prop(context.scene, 'RSNBusyDrawing', text='Drawing...', toggle=1, icon='GREASEPENCIL')
        else:
            row.operator("rsn.draw_nodes", icon='GREASEPENCIL')

        pref = get_pref()
        row.prop(pref.draw_nodes, 'show_text_info', text='', icon="INFO")


def register():
    bpy.types.NODE_MT_editor_menus.append(draw_item)


def unregister():
    bpy.types.NODE_MT_editor_menus.remove(draw_item)
