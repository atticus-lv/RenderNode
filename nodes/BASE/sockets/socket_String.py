import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node



class RenderNodeSocketString(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketString'
    bl_label = 'RenderNodeSocketString'

    default_value: StringProperty(default='', update=update_node)

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1


class RenderNodeSocketFilePath(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketFilePath'
    bl_label = 'RenderNodeSocketFilePath'

    default_value: StringProperty(default='', update=update_node, subtype='FILE_PATH')

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1



class RenderNodeSocketViewLayer(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketViewLayer'
    bl_label = 'RenderNodeSocketViewLayer'

    default_value: StringProperty(update=update_node)

    def draw(self, context, layout, node, text):

        row = layout.row(align=1)
        if self.is_linked or self.is_output:
            row.label(text=self.display_name)
        else:
            row.prop_search(self, "default_value", context.scene, "view_layers", text='')

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1



classes = (
    RenderNodeSocketViewLayer,
    RenderNodeSocketString,
    RenderNodeSocketFilePath,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
