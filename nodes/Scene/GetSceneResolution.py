import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetSceneResolution(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetSceneResolution'
    bl_label = 'Get Scene Resolution'

    def init(self, context):
        self.create_output('RenderNodeSocketInt', 'resolution_x', 'x')
        self.create_output('RenderNodeSocketInt', 'resolution_y', 'y')
        self.create_output('RenderNodeSocketInt', 'resolution_percentage', '%')

    def process(self, context, id, path):
        for output in self.outputs:
            output.set_value(getattr(context.scene.render, output.name))


def register():
    bpy.utils.register_class(RenderNodeGetSceneResolution)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetSceneResolution)
