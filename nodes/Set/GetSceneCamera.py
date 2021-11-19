import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetSceneCamera(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetSceneCamera'
    bl_label = 'Get Scene Camera'

    def init(self, context):
        self.create_output('RenderNodeSocketObject', 'camera', 'Camera')


    def process(self, context, id, path):
        self.outputs['camera'].set_value(context.scene.camera)


def register():
    bpy.utils.register_class(RenderNodeGetSceneCamera)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetSceneCamera)
