import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RSNodeNullNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodeNullNode'
    bl_label = 'Null'

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'name')


def register():
    bpy.utils.register_class(RSNodeNullNode)


def unregister():
    bpy.utils.unregister_class(RSNodeNullNode)
