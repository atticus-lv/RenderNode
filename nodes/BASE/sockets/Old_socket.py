import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node





class RSNodeSocketCamera(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketCamera'
    bl_label = 'RSN Camera'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0.6, 0.6, 0.6, 1.0


class RSNodeSocketRenderSettings(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketRenderSettings'
    bl_label = 'RSN RenderSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0, 1, 0.5, 1.0


class RSNodeSocketOutputSettings(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketOutputSettings'
    bl_label = 'RSN OutputSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 1, 0.8, 0.2, 1.0





classes = (
    RSNodeSocketCamera,
    RSNodeSocketRenderSettings,
    RSNodeSocketOutputSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
