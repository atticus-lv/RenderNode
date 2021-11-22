import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetCyclesLightPathsMaxBounces(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesLightPathsMaxBounces'
    bl_label = 'Set Cycles Light Paths Max Bounces'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketInt', 'max_bounces', 'Total', default_value=12)
        self.create_input('RenderNodeSocketInt', 'diffuse_bounces', 'Diffuse', default_value=4)
        self.create_input('RenderNodeSocketInt', 'glossy_bounces', 'Glossy', default_value=4)
        self.create_input('RenderNodeSocketInt', 'transparent_max_bounces', 'Transparency', default_value=8)
        self.create_input('RenderNodeSocketInt', 'transmission_bounces', 'Transmission', default_value=12)
        self.create_input('RenderNodeSocketInt', 'volume_bounces', 'Volume', default_value=0)
        self.create_input('RenderNodeSocketFloat', 'sample_clamp_direct', 'Direct Light', default_value=0)
        self.create_input('RenderNodeSocketFloat', 'sample_clamp_indirect', 'Indirect Light', default_value=0)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        if not self.process_task(): return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(bpy.context.scene.cycles, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesLightPathsMaxBounces)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesLightPathsMaxBounces)
