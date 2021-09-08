import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceScene(RenderNodeSocketmixin, RenderNodeSocketInterface, bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketWorld'
    bl_socket_idname = 'RenderNodeSocketWorld'
    bl_label = 'Scene (RenderNode)'

    default_value: FloatVectorProperty(name='Default Value')

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return 1, 0.4, 0.4, 1


class RenderNodeSocketScene(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketScene'
    bl_label = 'RenderNodeSocketScene'

    default_value: PointerProperty(type=bpy.types.Scene, update=update_node)

    def draw_color(self, context, node):
        return 1, 0.4, 0.4, 1


classes = (
    RenderNodeSocketInterfaceScene,
    RenderNodeSocketScene,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
