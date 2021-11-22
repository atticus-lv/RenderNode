import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetSceneWorld(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetSceneWorld'
    bl_label = 'Get Scene World'

    def init(self, context):
        self.create_output('RenderNodeSocketWorld', 'world', 'World')

    def process(self, context, id, path):
        self.outputs['world'].set_value(context.scene.world)


def register():
    bpy.utils.register_class(RenderNodeGetSceneWorld)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetSceneWorld)
