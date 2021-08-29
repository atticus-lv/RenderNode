import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceWorld(RenderNodeSocketmixin, RenderNodeSocketInterface, bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketWorld'
    bl_socket_idname = 'RenderNodeSocketWorld'
    bl_label = 'World (RenderNode)'

    default_value: FloatVectorProperty(name='Default Value')

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return 1, 0.4, 0.4, 1


class RenderNodeSocketWorld(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketWorld'
    bl_label = 'RenderNodeSocketWorld'

    default_value: PointerProperty(type=bpy.types.World, update=update_node)

    def draw_color(self, context, node):
        return 1, 0.4, 0.4, 1


classes = (
    RenderNodeSocketInterfaceWorld,
    RenderNodeSocketWorld,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
