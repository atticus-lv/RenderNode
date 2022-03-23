import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


class RenderNodeInt2Str(RenderNodeBase):
    bl_idname = 'RenderNodeInt2Str'
    bl_label = 'Int 2 Str'

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'int', 'Int')
        self.create_output('RenderNodeSocketString', 'str', "String")

    def process(self, context, id, path):
        i = self.inputs[0].get_value()
        if i is not None: self.outputs[0].set_value(str(int(i)))


def register():
    bpy.utils.register_class(RenderNodeInt2Str)


def unregister():
    bpy.utils.unregister_class(RenderNodeInt2Str)
