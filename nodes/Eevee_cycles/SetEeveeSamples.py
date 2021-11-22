import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetEeveeSamples(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetEeveeSamples'
    bl_label = 'Set Eevee Samples'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketInt', 'taa_render_samples', 'Render', default_value=64)
        self.create_input('RenderNodeSocketInt', 'taa_samples', 'Viewport', default_value=64)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')


    def process(self, context, id, path):
        if not self.process_task():return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.eevee, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetEeveeSamples)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetEeveeSamples)
