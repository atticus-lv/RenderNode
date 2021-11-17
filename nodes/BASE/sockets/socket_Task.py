import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceTask(RenderNodeSocketmixin, RenderNodeSocketInterface, bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketTask'
    bl_socket_idname = 'RenderNodeSocketTask'
    bl_label = 'Task (RenderNode)'


    def draw(self, context, layout):
        pass

    def draw_color(self, context):
        return 0, 0.8, 0.1, 1


class RenderNodeSocketTask(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketTask'
    bl_label = 'Task (RenderNode)'

    compatible_sockets = ['RenderNodeSocketTask']

    default_value: StringProperty(default='', update=update_node)

    def draw(self, context, layout, node, text):
        layout.label(text='Task')


    def draw_color(self, context, node):
        return 0, 0.8, 0.1, 1


classes = (
    RenderNodeSocketInterfaceTask,
    RenderNodeSocketTask,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
