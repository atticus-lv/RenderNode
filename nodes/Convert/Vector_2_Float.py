import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


class RenderNodeVector2Float(RenderNodeBase):
    bl_idname = 'RenderNodeVector2Float'
    bl_label = 'Vector 2 Float'


    def init(self, context):
        self.create_output('RenderNodeSocketFloat', 'x', 'X')
        self.create_output('RenderNodeSocketFloat', 'y', 'Y')
        self.create_output('RenderNodeSocketFloat', 'z', 'Z')
        self.create_input('RenderNodeSocketXYZ', 'vector', "Vector")

    def process(self, context, id, path):

        input_value = list(self.inputs[0].get_value())
        self.outputs[0].set_value(input_value[0])
        self.outputs[1].set_value(input_value[1])
        self.outputs[2].set_value(input_value[2])


def register():
    bpy.utils.register_class(RenderNodeVector2Float)


def unregister():
    bpy.utils.unregister_class(RenderNodeVector2Float)
