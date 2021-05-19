import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RenderNodeObjectInput(RenderStackNode):
    bl_idname = 'RenderNodeMaterialInput'
    bl_label = 'Material Input'

    value: PointerProperty(type=bpy.types.Material)

    def init(self, context):
        self.outputs.new('NodeSocketMaterial', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value',text='')


def register():
    bpy.utils.register_class(RenderNodeObjectInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectInput)
