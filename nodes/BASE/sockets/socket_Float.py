import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceFloat(RenderNodeSocketmixin, RenderNodeSocketInterface,
                                     bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketFloat'
    bl_socket_idname = 'RenderNodeSocketFloat'
    bl_label = 'Float (RenderNode)'

    default_value: FloatProperty(name='Default Value')

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return 0.5, 0.5, 0.5, 1


class RenderNodeSocketFloat(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketFloat'
    bl_label = 'RenderNodeSocketFloat'

    compatible_sockets = ['RenderNodeSocketInt']
    
    default_value: FloatProperty(default=0, update=update_node)

    def draw_color(self, context, node):
        return 0.5, 0.5, 0.5, 1


classes = (
    RenderNodeSocketInterfaceFloat,
    RenderNodeSocketFloat,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
