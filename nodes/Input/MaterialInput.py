import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class RenderNodeObjectInput(RenderNodeBase):
    bl_idname = 'RenderNodeMaterialInput'
    bl_label = 'Material Input'

    default_value: PointerProperty(type=bpy.types.Material, update=update_node)

    def init(self, context):
        self.create_output('RenderNodeSocketMaterial', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.scale_y = 0.75
        layout.scale_x = 0.75
        layout.template_ID_preview(
            self, "default_value",
            rows=3, cols=4, hide_buttons=False)

    def process(self,context,id,path):
        self.outputs[0].set_value(self.default_value)


def register():
    bpy.utils.register_class(RenderNodeObjectInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectInput)
