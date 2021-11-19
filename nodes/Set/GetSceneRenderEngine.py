import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetSceneRenderEngine(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetSceneRenderEngine'
    bl_label = 'Get Scene Render Engine'

    def init(self, context):
        self.create_output('RenderNodeSocketString', 'name', 'Name')

    def process(self, context, id, path):
        self.outputs['name'].set_value(context.scene.render.engine)


def register():
    bpy.utils.register_class(RenderNodeGetSceneRenderEngine)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetSceneRenderEngine)
