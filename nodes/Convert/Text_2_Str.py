import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


class RenderNodeText2Str(RenderNodeBase):
    bl_idname = 'RenderNodeText2Str'
    bl_label = 'Text 2 Str'

    def init(self, context):
        self.create_output('RenderNodeSocketString', 'str', "String")
        self.create_input('RenderNodeSocketText', 'text', 'Text')

    def process(self, context, id, path):
        res = None
        text = self.inputs['text'].get_value()
        if text:
            res = text.as_string()
        self.outputs[0].set_value(res)


def register():
    bpy.utils.register_class(RenderNodeText2Str)


def unregister():
    bpy.utils.unregister_class(RenderNodeText2Str)
