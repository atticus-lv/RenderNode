import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RenderNodeStringInput(RenderStackNode):
    bl_idname = 'RenderNodeStringInput'
    bl_label = 'String Input +'

    value: StringProperty()

    def init(self, context):
        self.outputs.new('NodeSocketString', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value', text='')


def register():
    bpy.utils.register_class(RenderNodeStringInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeStringInput)
