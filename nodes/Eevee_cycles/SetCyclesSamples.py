import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

def update_node(self, context):
    self.execute_tree()


class RenderNodeSetCyclesSamples(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesSamples'
    bl_label = 'Set Cycles Samples (2.93)'

    use_denoising: BoolProperty()
    use_preview_denoising: BoolProperty()

    denoiser: EnumProperty(items=[
        ('NLM', 'NLM', ''),
        ('OPTIX', 'Optix', ''),
        ('OPENIMAGEDENOISE', 'OpenImageDenoise', '')
    ], default='NLM',name = "Denoiser",update=update_node)

    preview_denoiser: EnumProperty(items=[
        ('OPTIX', 'Optix', ''),
        ('OPENIMAGEDENOISE', 'OpenImageDenoise', ''),
    ], default='OPTIX',name = "Viewport Denoiser",update=update_node)

    preview_denoising_input_passes: EnumProperty(items=[
        ('RGB', 'Color', ''),
        ('RGB_ALBEDO', 'Color + Albedo', ''),
        ('RGB_ALBEDO_NORMAL', 'Color + Albedo + Normal', ''),
    ], default='RGB',name = "Passes",update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketInt', 'preview_samples', 'Viewport Samples', default_value=1024)
        self.create_input('RenderNodeSocketInt', 'samples', 'Render Samples', default_value=1024)

        self.create_input('RenderNodeSocketBool', 'use_adaptive_sampling', 'Use Adaptive Sampling',
                          default_value=False)
        self.create_input('RenderNodeSocketFloat', 'adaptive_threshold', 'Noise Threshold',
                          default_value=0.01)
        self.create_input('RenderNodeSocketInt', 'adaptive_min_samples', 'Min Samples', default_value=0)

        self.create_input('RenderNodeSocketBool', 'use_denoising', 'Use Denoising', default_value=False)
        self.create_input('RenderNodeSocketBool', 'use_preview_denoising', 'Use Viewport Denoising',
                          default_value=False)
        self.create_input('RenderNodeSocketInt', 'preview_denoising_start_sample', 'Start Sample', default_value=1)
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 220

    def draw_buttons(self, context, layout):
        if self.use_denoising is True:
            layout.prop(self, 'denoiser')

        if self.use_preview_denoising is True:
            layout.prop(self, 'preview_denoiser')
            layout.prop(self, 'preview_denoising_input_passes')

    def process(self, context, id, path):
        if not self.process_task(): return

        use_preview_denoising = self.inputs['use_preview_denoising'].get_value()
        if use_preview_denoising is True:
            self.use_preview_denoising = True

        use_denoising = self.inputs['use_denoising'].get_value()
        if use_denoising is True:
            self.use_denoising = True

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.cycles, key, value)

        self.compare(context.scene.cycles, 'denoiser', self.denoiser)
        self.compare(context.scene.cycles, 'preview_denoiser', self.preview_denoiser)
        self.compare(context.scene.cycles, 'preview_denoising_input_passes', self.preview_denoising_input_passes)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesSamples)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesSamples)
