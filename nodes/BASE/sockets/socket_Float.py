import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


class RenderNodeSocketFloat(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketFloat'
    bl_label = 'RenderNodeSocketFloat'

    default_value: FloatProperty(default=0, update=update_node)

    def draw_color(self, context, node):
        return 0.5, 0.5, 0.5, 1


classes = (
    RenderNodeSocketFloat,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
