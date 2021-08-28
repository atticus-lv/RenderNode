import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


class RenderNodeSocketCollection(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketCollection'
    bl_label = 'RenderNodeSocketCollection'

    default_value: PointerProperty(type=bpy.types.Collection, update=update_node)

    def draw_color(self, context, node):
        return 1, 1, 1, 0.5



classes = (
    RenderNodeSocketCollection,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
