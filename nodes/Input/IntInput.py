import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RenderNodeIntInput(RenderNodeBase):
    bl_idname = 'RenderNodeIntInput'
    bl_label = 'Int Input'

    default_value: IntProperty(update=update_node)

    def init(self, context):
        self.create_output('RenderNodeSocketInt', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'default_value', text='')

    def process(self):
        self.outputs[0].set_value(round(self.default_value,2))


def register():
    bpy.utils.register_class(RenderNodeIntInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeIntInput)
