import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceCollection(RenderNodeSocketmixin, RenderNodeSocketInterface,
                                          bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketCollection'
    bl_socket_idname = 'RenderNodeSocketCollection'
    bl_label = 'Collection (RenderNode)'

    default_value: PointerProperty(name='Default Value', type=bpy.types.Collection)

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return (1, 1, 1, 0.5)


class RenderNodeSocketCollection(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketCollection'
    bl_label = 'RenderNodeSocketCollection'

    default_value: PointerProperty(type=bpy.types.Collection, update=update_node)

    def draw_color(self, context, node):
        return (1, 1, 1, 0.5)


classes = (
    RenderNodeSocketCollection,
    RenderNodeSocketInterfaceCollection,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
