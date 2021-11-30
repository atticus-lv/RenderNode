import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

def update_node(self, context):
    self.execute_tree()

class RenderNodeSetCyclesSamplesRender(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesSamplesRender'
    bl_label = 'Set Cycles Samples Render'

    use_denoising: BoolProperty()

    denoiser: EnumProperty(items=[
        ('OPTIX', 'Optix', ''),
        ('OPENIMAGEDENOISE', 'OpenImageDenoise', ''),
    ], default='OPTIX',name = "Denoiser",update = update_node)

    denoising_input_passes: EnumProperty(items=[
        ('RGB', 'Color', ''),
        ('RGB_ALBEDO', 'Color + Albedo', ''),
        ('RGB_ALBEDO_NORMAL', 'Color + Albedo + Normal', ''),
    ], default='RGB',name='Passes',update = update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_adaptive_sampling', 'Use Adaptive Sampling',
                          default_value=True)
        self.create_input('RenderNodeSocketFloat', 'adaptive_threshold', 'Noise Threshold',
                          default_value=0.01)
        self.create_input('RenderNodeSocketInt', 'samples', 'Viewport Samples', default_value=1024)
        self.create_input('RenderNodeSocketInt', 'adaptive_min_samples', 'Min Samples', default_value=0)
        self.create_input('RenderNodeSocketInt', 'time_limit', 'Time Limit', default_value=0)
        self.create_input('RenderNodeSocketBool', 'use_denoising', 'Use Denoising', default_value=False)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 220

    def draw_buttons(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False

        if self.use_denoising is True:
            layout.prop(self, 'denoiser')
            layout.prop(self, 'denoising_input_passes')

    def process(self, context, id, path):
        if not self.process_task(): return

        use_denoising = self.inputs['use_denoising'].get_value()

        self.use_denoising = True if use_denoising else False

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.cycles, key, value)

        self.compare(context.scene.cycles, 'denoiser', self.denoiser)
        self.compare(context.scene.cycles, 'denoising_input_passes', self.denoising_input_passes)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesSamplesRender)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesSamplesRender)
