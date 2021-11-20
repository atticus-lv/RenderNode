import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetCyclesLightPathsCaustics(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesLightPathsCaustics'
    bl_label = 'Set Cycles Light Paths Caustics'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketFloat', 'blur_glossy', 'Filter Glossy', default_value=1)
        self.create_input('RenderNodeSocketBool', 'caustics_reflective', 'Reflective', default_value=True)
        self.create_input('RenderNodeSocketBool', 'caustics_refractive', 'Refractive', default_value=True)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        if not self.process_task(): return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(bpy.context.scene.cycles, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesLightPathsCaustics)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesLightPathsCaustics)
