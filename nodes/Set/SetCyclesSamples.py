import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetCyclesSamples(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesSamples'
    bl_label = 'Set Cycles Samples'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketFloat', 'preview_adaptive_threshold', 'Viewport Noise Threshold',
                          default_value=0.01)
        self.create_input('RenderNodeSocketInt', 'preview_samples', 'Viewport Samples', default_value=1024)
        self.create_input('RenderNodeSocketInt', 'preview_adaptive_min_samples', 'Viewport Min Samples',
                          default_value=0)

        self.create_input('RenderNodeSocketFloat', 'adaptive_threshold', 'Render Noise Threshold',
                          default_value=0.01)
        self.create_input('RenderNodeSocketFloat', 'time_limit', 'Render Time Limit', default_value=0)
        self.create_input('RenderNodeSocketInt', 'samples', 'Render Samples', default_value=1024)
        self.create_input('RenderNodeSocketInt', 'adaptive_min_samples', 'Render Min Samples', default_value=0)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 220

    def process(self, context, id, path):
        if not self.process_task():return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(bpy.context.scene.cycles, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesSamples)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesSamples)
