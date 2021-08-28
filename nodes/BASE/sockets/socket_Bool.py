import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


# class RenderNodeSocketInterfaceBool(bpy.types.NodeSocketInterface):
#     bl_idname = 'RenderNodeSocketBool'
#     bl_socket_idname = 'Bool(RenderNode)'
#
#     def draw(self, context, layout):
#         if hasattr(self, 'default_value'):
#             layout.prop(self, 'text')
#             layout.prop(self, 'default_value')
#
#     def draw_color(self, context):
#         return 0.9, 0.7, 1.0, 1


class RenderNodeSocketBool(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketBool'
    bl_label = 'Bool(RenderNode)'

    default_value: BoolProperty(default=False, update=update_node)

    def draw_color(self, context, node):
        return 0.9, 0.7, 1.0, 1


classes = (
    # RenderNodeSocketInterfaceBool,
    RenderNodeSocketBool,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
