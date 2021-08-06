import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RenderNodeStringCombine(RenderNodeBase):
    bl_idname = 'RenderNodeStringCombine'
    bl_label = 'String Combine'

    def init(self, context):
        self.creat_input('RenderNodeSocketString', 'value1', 'Value')
        self.creat_input('RenderNodeSocketString', 'value2', 'Value')
        self.creat_output('RenderNodeSocketString', 'output', "Output")

    def draw_buttons(self, context, layout):
        pass

    def process(self):
        s1 = self.inputs['value1'].get_value()
        s2 = self.inputs['value2'].get_value()
        self.outputs[0].set_value(s1 + s2)


def register():
    bpy.utils.register_class(RenderNodeStringCombine)


def unregister():
    bpy.utils.unregister_class(RenderNodeStringCombine)
