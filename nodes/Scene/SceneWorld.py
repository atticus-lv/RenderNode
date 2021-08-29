import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSceneWorld(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneWorld'
    bl_label = 'Scene World'

    def init(self, context):
        self.create_input('RenderNodeSocketWorld', "world", 'World')

        self.create_output('RSNodeSocketTaskSettings','Settings','Settings')

    def process(self,context,id,path):
        world = self.inputs['world'].get_value()

        if world:
            self.compare(bpy.context.scene, 'world', world)


def register():
    bpy.utils.register_class(RenderNodeSceneWorld)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneWorld)
