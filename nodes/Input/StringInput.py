import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class RenderNodeStringInput(RenderNodeBase):
    bl_idname = 'RenderNodeStringInput'
    bl_label = 'String Input'

    default_value: StringProperty(update=update_node)

    def init(self, context):
        self.create_output('RenderNodeSocketString', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'default_value', text='')

    def process(self,context,id,path):
        self.outputs[0].set_value(self.default_value)


def register():
    bpy.utils.register_class(RenderNodeStringInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeStringInput)
