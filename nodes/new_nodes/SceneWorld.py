import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


class RenderNodeSceneWorld(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneWorld'
    bl_label = 'Scene World'

    def init(self, context):
        self.create_prop('RenderNodeSocketWorld', "world", 'World')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def process(self):
        self.store_data()
        world = self.node_dict['world']

        if world:
            self.compare(bpy.context.scene, 'world', world)


def register():
    bpy.utils.register_class(RenderNodeSceneWorld)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneWorld)
