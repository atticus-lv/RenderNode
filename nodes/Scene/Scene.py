import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeScene(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeScene'
    bl_label = 'Scene'

    def init(self, context):
        self.create_input('RenderNodeSocketScene', "scn", 'Scene')
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')

    def process(self, context, id, path):
        scn = self.inputs[0].get_value()
        if scn: self.compare(context.window, 'scene', scn)


def register():
    bpy.utils.register_class(RenderNodeScene)


def unregister():
    bpy.utils.unregister_class(RenderNodeScene)
