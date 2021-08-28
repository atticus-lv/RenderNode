import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


class RenderNodeSocketMaterial(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketMaterial'
    bl_label = 'RenderNodeSocketMaterial'

    default_value: PointerProperty(type=bpy.types.Material, update=update_node)

    def draw_color(self, context, node):
        return 1, 0.4, 0.4, 1


classes = (
    RenderNodeSocketMaterial,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
