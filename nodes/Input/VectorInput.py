import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class RenderNodeVectorInput(RenderNodeBase):
    bl_idname = 'RenderNodeVectorInput'
    bl_label = 'Vector Input'

    default_value: FloatVectorProperty(update=update_node)

    def init(self, context):
        self.create_output('RenderNodeSocketXYZ', 'output', "Output")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, 'default_value', text='')

    def process(self,context,id,path):
        self.outputs[0].set_value(Vector((self.default_value[0],self.default_value[1],self.default_value[2])))


def register():
    bpy.utils.register_class(RenderNodeVectorInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeVectorInput)
