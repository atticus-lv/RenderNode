import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.update_parms()


class RenderNodeObjectInput(RenderNodeBase):
    bl_idname = 'RenderNodeObjectInput'
    bl_label = 'Object Input'

    default_value: PointerProperty(type=bpy.types.Object, update=update_node)

    def init(self, context):
        self.creat_output('RenderNodeSocketObject', "output", "Output")

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.prop(self, 'default_value', text='')
        if self.default_value:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.default_value.name

    def process(self):
        self.outputs[0].set_value(self.default_value)


def register():
    bpy.utils.register_class(RenderNodeObjectInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectInput)
