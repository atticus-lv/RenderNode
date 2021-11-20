import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetEeveeScreenSpaceReflections(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetEeveeScreenSpaceReflections'
    bl_label = 'Set Eevee Screen Space Reflections'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_ssr', 'Enable', default_value=False)
        self.create_input('RenderNodeSocketBool', 'use_ssr_refraction', 'Refraction', default_value=True)
        self.create_input('RenderNodeSocketFloat', 'ssr_quality', 'Trace Precision', default_value=0.25)
        self.create_input('RenderNodeSocketFloat', 'ssr_max_roughness', 'Max Roughness', default_value=0.25)
        self.create_input('RenderNodeSocketFloat', 'ssr_thickness', 'Thickness', default_value=0.2)
        self.create_input('RenderNodeSocketFloat', 'ssr_border_fade', 'Edge Fading', default_value=0.075)
        self.create_input('RenderNodeSocketFloat', 'ssr_firefly_fac', 'Clamp', default_value=10)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        if not self.process_task(): return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(bpy.context.scene.eevee, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetEeveeScreenSpaceReflections)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetEeveeScreenSpaceReflections)
