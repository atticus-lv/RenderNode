import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


class RenderNodeSocketInt(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketInt'
    bl_label = 'RenderNodeSocketInt'

    default_value: IntProperty(default=0, update=update_node)

    def draw_color(self, context, node):
        return 0, 0.9, 0.1, 1

classes = (
    RenderNodeSocketInt,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
