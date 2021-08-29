import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceText(RenderNodeSocketmixin, RenderNodeSocketInterface, bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketText'
    bl_socket_idname = 'RenderNodeSocketText'
    bl_label = 'Text (RenderNode)'

    default_value: PointerProperty(name='Default Value', type=bpy.types.Text)

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return 0.2, 0.7, 1.0, 1


class RenderNodeSocketText(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketText'
    bl_label = 'RenderNodeSocketText'

    default_value: PointerProperty(update=update_node, type=bpy.types.Text)

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1


classes = (
    RenderNodeSocketInterfaceText,
    RenderNodeSocketText,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
