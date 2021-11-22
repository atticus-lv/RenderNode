import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetEeveeBloom(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetEeveeBloom'
    bl_label = 'Set Eevee Bloom'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_bloom', 'Enable', default_value=False)
        self.create_input('RenderNodeSocketFloat', 'bloom_threshold', 'Threshold', default_value=0.8)
        self.create_input('RenderNodeSocketFloat', 'bloom_knee', 'Knee', default_value=0.5)
        self.create_input('RenderNodeSocketFloat', 'bloom_radius', 'Radius', default_value=6.5)
        self.create_input('RenderNodeSocketColor', 'bloom_color', 'Color', default_value=(1,1,1))
        self.create_input('RenderNodeSocketFloat', 'bloom_intensity', 'Intensity', default_value=0.05)
        self.create_input('RenderNodeSocketFloat', 'bloom_clamp', 'Clamp')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')


    def process(self, context, id, path):
        if not self.process_task():return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.eevee, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetEeveeBloom)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetEeveeBloom)
