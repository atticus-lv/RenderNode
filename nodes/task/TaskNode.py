import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeTaskNode(RenderStackNode):
    '''A simple Task node'''
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        layout.prop(self, 'label', text="Label")


def register():
    bpy.utils.register_class(RSNodeTaskNode)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)
