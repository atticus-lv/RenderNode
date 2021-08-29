import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class RenderNodeBoolInput(RenderNodeBase):
    bl_idname = 'RenderNodeBoolInput'
    bl_label = 'Bool Input'

    default_value: BoolProperty(update=update_node)

    def init(self, context):
        self.create_output('RenderNodeSocketBool', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'default_value', text='')

    def process(self,context,id,path):
        self.outputs[0].set_value(self.default_value)


def register():
    bpy.utils.register_class(RenderNodeIntInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeIntInput)
