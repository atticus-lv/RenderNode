import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetSceneSimplify(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneSimplify'
    bl_label = 'Set Scene Simplify'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_simplify', 'Enable', default_value=False)
        self.create_input('RenderNodeSocketInt', 'simplify_subdivision', 'Max Subdivision', default_value=6)
        self.create_input('RenderNodeSocketFloat', 'simplify_child_particles', 'Max Child Particles',default_value=1)
        self.create_input('RenderNodeSocketFloat', 'simplify_volumes', 'Volumes Resolution',default_value=1)

        self.create_input('RenderNodeSocketInt', 'simplify_subdivision_render', 'Render Max Subdivision', default_value=6)
        self.create_input('RenderNodeSocketFloat', 'simplify_child_particles_render', 'Render Max Child Particles', default_value=1)


        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 200

    def process(self, context, id, path):
        if not self.process_task(): return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.render, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetSceneSimplify)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetSceneSimplify)
