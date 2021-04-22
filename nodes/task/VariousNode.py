import bpy
from bpy.props import *
from ..BASE.node_tree import RenderStackNode
from ...utility import *

class RSNodeVariousNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeVariousNode'
    bl_label = 'Various'

    # active: IntProperty(default=0, min=0, update=update_node)

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'name')
        # layout.prop(self, 'active')

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Input")

    def auto_update_inputs(self, socket_type, socket_name):
        super().auto_update_inputs(socket_type, socket_name)

    def get_active(self):
        pass

def register():
    bpy.utils.register_class(RSNodeVariousNode)


def unregister():
    bpy.utils.unregister_class(RSNodeVariousNode)
