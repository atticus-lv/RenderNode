import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetEeveeAmbientOcclusion(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetEeveeAmbientOcclusion'
    bl_label = 'Set Eevee Ambient Occlusion'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_gtao', 'Enable', default_value=False)
        self.create_input('RenderNodeSocketFloat', 'gtao_distance', 'Distance', default_value=0.2)
        self.create_input('RenderNodeSocketFloat', 'gtao_factor', 'Factor', default_value=1)
        self.create_input('RenderNodeSocketFloat', 'gtao_quality', 'Trace Precision', default_value=0.25)
        self.create_input('RenderNodeSocketBool', 'use_gtao_bent_normals', 'Bent Normals', default_value=True)
        self.create_input('RenderNodeSocketBool', 'use_gtao_bounce', 'Bounces Approximation', default_value=True)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')


    def process(self, context, id, path):
        if not self.process_task():return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(bpy.context.scene.eevee, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetEeveeAmbientOcclusion)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetEeveeAmbientOcclusion)
