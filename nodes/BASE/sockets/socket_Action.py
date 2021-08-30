import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceAction(RenderNodeSocketmixin, RenderNodeSocketInterface, bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketAction'
    bl_socket_idname = 'RenderNodeSocketAction'
    bl_label = 'Action (RenderNode)'

    default_value: PointerProperty(name='Default Value', type=bpy.types.Action)

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return (0.9, 0.7, 1.0, 1)


class RenderNodeSocketAction(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketAction'
    bl_label = 'Action (RenderNode)'

    default_value: PointerProperty(name='Default Value', type=bpy.types.Action, update=update_node)

    def draw_color(self, context, node):
        return (0.78, 0.18, 0.38, 1)


classes = (
    RenderNodeSocketInterfaceAction,
    RenderNodeSocketAction,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
