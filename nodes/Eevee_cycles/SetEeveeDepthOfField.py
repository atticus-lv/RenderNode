import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetEeveeDepthOfField(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetEeveeDepthOfField'
    bl_label = 'Set Eevee Depth Of Field'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketFloat', 'bokeh_max_size', 'Max Size', default_value=100)
        self.create_input('RenderNodeSocketFloat', 'bokeh_threshold', 'Sprite Threshold', default_value=1)
        self.create_input('RenderNodeSocketFloat', 'bokeh_neighbor_max', 'Neighbor Rejection', default_value=10)
        self.create_input('RenderNodeSocketFloat', 'bokeh_denoise_fac', 'Denoise Amount', default_value=6.5)
        self.create_input('RenderNodeSocketBool', 'use_bokeh_high_quality_slight_defocus',
                          'High Quality Slight Defocus', default_value=False)
        self.create_input('RenderNodeSocketBool', 'use_bokeh_jittered', 'Jitter Camera', default_value=False)
        self.create_input('RenderNodeSocketFloat', 'bokeh_overblur', 'Over-blur', default_value=5)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 200
    def process(self, context, id, path):
        if not self.process_task(): return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.eevee, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetEeveeDepthOfField)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetEeveeDepthOfField)
