import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


class RSNodeSocketRenderList(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketRenderList'
    bl_label = 'RSNodeSocketRenderList'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0.95, 0.95, 0.95, 1.0


classes = (
    RSNodeSocketRenderList,

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
