import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetSceneWorld(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneWorld'
    bl_label = 'Set Scene World'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_input('RenderNodeSocketWorld', "world", 'World')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self,context,id,path):
        self.process_task()
        world = self.inputs['world'].get_value()

        if world:
            self.compare(bpy.context.scene, 'world', world)


def register():
    bpy.utils.register_class(RenderNodeSetSceneWorld)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetSceneWorld)
