import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetCyclesLightPathsClamping(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesLightPathsClamping'
    bl_label = 'Set Cycles Light Paths Clamping'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

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
    bpy.utils.register_class(RenderNodeSetCyclesLightPathsClamping)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesLightPathsClamping)
