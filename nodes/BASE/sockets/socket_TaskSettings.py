import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


class RenderNodeSocketInterfaceTaskSettings(RenderNodeSocketmixin, RenderNodeSocketInterface,
                                          bpy.types.NodeSocketInterface):
    bl_idname = 'RSNodeSocketTaskSettings'
    bl_socket_idname = 'RSNodeSocketTaskSettings'
    bl_label = 'TaskSettings (RenderNode)'

    def draw(self, context, layout):
        pass

    def draw_color(self, context):
        return 0.6, 0.6, 0.6, 1.0


class RSNodeSocketTaskSettings(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketTaskSettings'
    bl_label = 'RSNodeSocketTaskSettings'

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            io = layout.operator('rsn.search_and_link', text=text, icon='ADD')
            io.node_name = node.name
            if self.is_output:
                io.output_id = int(self.path_from_id()[-2:-1])
                io.input_id = 666
            else:
                io.input_id = int(self.path_from_id()[-2:-1])
                io.output_id = 666
        else:
            layout.label(text=text)

    def draw_color(self, context, node):
        return 0.6, 0.6, 0.6, 1.0


classes = (
    RenderNodeSocketInterfaceTaskSettings,
    RSNodeSocketTaskSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
