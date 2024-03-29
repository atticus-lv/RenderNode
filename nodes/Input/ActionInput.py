import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class RenderNodeActionInput(RenderNodeBase):
    bl_idname = 'RenderNodeActionInput'
    bl_label = 'Action Input'

    default_value: PointerProperty(type=bpy.types.Action, update=update_node)

    def init(self, context):
        self.create_output('RenderNodeSocketAction', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'default_value', text='')

    def process(self, context, id, path):
        self.outputs[0].set_value(self.default_value)


def register():
    bpy.utils.register_class(RenderNodeActionInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeActionInput)
