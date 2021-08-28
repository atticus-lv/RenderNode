import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


class RenderNodeSocketText(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketText'
    bl_label = 'RenderNodeSocketText'

    default_value: PointerProperty(update=update_node, type=bpy.types.Text)

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1


classes = (
    RenderNodeSocketText,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
