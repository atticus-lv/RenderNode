import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RenderNodeObjectInput(RenderNodeBase):
    bl_idname = 'RenderNodeObjectInput'
    bl_label = 'Object Input'

    value: PointerProperty(type=bpy.types.Object, update=update_node)

    def init(self, context):
        self.outputs.new('NodeSocketObject', "Output")

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.prop(self, 'value', text='')
        if self.value:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.value.name


def register():
    bpy.utils.register_class(RenderNodeObjectInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectInput)
