import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector



class RenderNodeFloat2Vector(RenderNodeBase):
    bl_idname = 'RenderNodeFloat2Vector'
    bl_label = 'Float 2 Vector'


    def init(self, context):
        self.create_input('RenderNodeSocketFloat', 'x', 'X')
        self.create_input('RenderNodeSocketFloat', 'y', 'Y')
        self.create_input('RenderNodeSocketFloat', 'z', 'Z')
        self.create_output('RenderNodeSocketXYZ', 'vector', "Vector")

    def process(self, context, id, path):
        res = Vector((
            self.inputs[0].get_value(),
            self.inputs[1].get_value(),
            self.inputs[2].get_value(),
        ))
        self.outputs[0].set_value(res)



def register():
    bpy.utils.register_class(RenderNodeFloat2Vector)


def unregister():
    bpy.utils.unregister_class(RenderNodeFloat2Vector)
