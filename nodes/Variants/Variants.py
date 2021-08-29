import bpy
from bpy.props import *
from ..BASE.node_base import RenderNodeBase
from ...utility import *


class RenderNodeVariants(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeVariants'
    bl_label = 'Variants'

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'active', "Active Input")
        self.create_input('RSNodeSocketTaskSettings', 'Settings', 'Settings')
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')

    # def draw_buttons(self, context, layout):
    #     layout.prop(self, 'name')

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Settings")

    def auto_update_inputs(self, socket_type, socket_name):
        super().auto_update_inputs(socket_type, socket_name, start_update_index=1)

    def process(self, context, id, path):
        active = self.inputs['active'].get_value()
        if not active: return
        for i, input in enumerate(self.inputs):
            _connected_socket = input.connected_socket
            if _connected_socket and _connected_socket.node is not None:
                if i == active:
                    _connected_socket.node.mute = False
                    if hasattr(_connected_socket.node, 'execute'): _connected_socket.node.execute(context, id, path)
                else:
                    _connected_socket.node.mute = True


def register():
    bpy.utils.register_class(RenderNodeVariants)


def unregister():
    bpy.utils.unregister_class(RenderNodeVariants)
