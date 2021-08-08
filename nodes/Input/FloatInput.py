import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RenderNodeFloatInput(RenderNodeBase):
    bl_idname = 'RenderNodeFloatInput'
    bl_label = 'Float Input'

    default_value: FloatProperty(update=update_node)

    def init(self, context):
        self.create_output('RenderNodeSocketFloat', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'default_value', text='')

    def process(self):
        self.outputs[0].set_value(self.default_value)


def register():
    bpy.utils.register_class(RenderNodeFloatInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeFloatInput)
