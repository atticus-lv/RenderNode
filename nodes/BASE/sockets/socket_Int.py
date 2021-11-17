import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceInt(RenderNodeSocketmixin, RenderNodeSocketInterface, bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketInt'
    bl_socket_idname = 'RenderNodeSocketInt'
    bl_label = 'Int (RenderNode)'

    default_value: IntProperty(name='Default Value')

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return (0.2, 0.65, 0.3, 1)



class RenderNodeSocketInt(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketInt'
    bl_label = 'RenderNodeSocketInt'
    
    compatible_sockets = ['RenderNodeSocketFloat','RenderNodeSocketBool']
    default_value: IntProperty(default=0, update=update_node)

    def draw_color(self, context, node):
        return (0.2, 0.65, 0.3, 1)


classes = (
    RenderNodeSocketInterfaceInt,
    RenderNodeSocketInt,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
