import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


class RenderNodeStr2Int(RenderNodeBase):
    bl_idname = 'RenderNodeStr2Int'
    bl_label = 'Str 2 Int'

    def init(self, context):
        self.create_output('RenderNodeSocketInt', 'int', 'Int')
        self.create_input('RenderNodeSocketString', 'str', "String")

    def process(self, context, id, path):
        s = self.inputs['str'].get_value()
        try:
            ans = int(s)
        except:
            ans = 0
        self.outputs[0].set_value(ans)


def register():
    bpy.utils.register_class(RenderNodeStr2Int)


def unregister():
    bpy.utils.unregister_class(RenderNodeStr2Int)
