import bpy
from bpy.props import *
from ..BASE.node_base import RenderNodeBase
from ...utility import *


class RSNodeVariantsNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodeVariantsNode'
    bl_label = 'Variants'

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'active', "Active Input")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    # def draw_buttons(self, context, layout):
    #     layout.prop(self, 'name')

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Settings")

    def auto_update_inputs(self, socket_type, socket_name):
        super().auto_update_inputs(socket_type, socket_name)

    def process(self, context, id, path):
        active = self.inputs['active'].get_value()
        if not active: return
        for i, input in enumerate(self.inputs):
            _connected_socket = input.connected_socket
            if _connected_socket and _connected_socket.node is not None:
                _connected_socket.node.mute = False if i == active else True


def register():
    bpy.utils.register_class(RSNodeVariantsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeVariantsNode)
