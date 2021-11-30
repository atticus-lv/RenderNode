import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

def update_node(self, context):
    self.execute_tree()

class RenderNodeSetCyclesSamplesViewport(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesSamplesViewport'
    bl_label = 'Set Cycles Samples Viewport'

    use_preview_denoising: BoolProperty()

    preview_denoiser: EnumProperty(items=[
        ('OPTIX', 'Optix', ''),
        ('OPENIMAGEDENOISE', 'OpenImageDenoise', ''),
    ], default='OPTIX',name = "Denoiser",update = update_node)

    preview_denoising_input_passes: EnumProperty(items=[
        ('RGB', 'Color', ''),
        ('RGB_ALBEDO', 'Color + Albedo', ''),
        ('RGB_ALBEDO_NORMAL', 'Color + Albedo + Normal', ''),
    ], default='RGB',name = 'Passes',update = update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_preview_adaptive_sampling', 'Use Adaptive Sampling',
                          default_value=True)
        self.create_input('RenderNodeSocketFloat', 'preview_adaptive_threshold', 'Noise Threshold',
                          default_value=0.01)
        self.create_input('RenderNodeSocketInt', 'preview_samples', 'Viewport Samples', default_value=1024)
        self.create_input('RenderNodeSocketInt', 'preview_adaptive_min_samples', 'Min Samples', default_value=0)
        self.create_input('RenderNodeSocketBool', 'use_preview_denoising', 'Use Viewport Denoising',
                          default_value=False)
        self.create_input('RenderNodeSocketInt', 'preview_denoising_start_sample', 'Start Sample', default_value=1)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 220

    def draw_buttons(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False

        if self.use_preview_denoising is True:
            layout.prop(self, 'preview_denoiser')
            layout.prop(self, 'preview_denoising_input_passes')

    def process(self, context, id, path):
        if not self.process_task(): return

        use_preview_denoising = self.inputs['use_preview_denoising'].get_value()

        self.use_preview_denoising = True if use_preview_denoising else False

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.cycles, key, value)

        self.compare(context.scene.cycles, 'preview_denoiser', self.preview_denoiser)
        self.compare(context.scene.cycles, 'preview_denoising_input_passes', self.preview_denoising_input_passes)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesSamplesViewport)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesSamplesViewport)
