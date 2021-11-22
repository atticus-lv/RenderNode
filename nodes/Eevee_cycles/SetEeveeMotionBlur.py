import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

def update_node(self, context):
    self.execute_tree()

class RenderNodeSetEeveeMotionBlur(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetEeveeMotionBlur'
    bl_label = 'Set Eevee Motion Blur'

    motion_blur_position: EnumProperty(items=[
        ('START', 'Start On Frame', ''),
        ('CENTER', 'Center On Frame', ''),
        ('END', 'End On Frame', ''),
    ], default='CENTER', name='Position',update =update_node )

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_motion_blur', 'Enable', default_value=False)
        self.create_input('RenderNodeSocketFloat', 'motion_blur_shutter', 'Shutter', default_value=0.5)
        self.create_input('RenderNodeSocketFloat', 'motion_blur_depth_scale', 'Background Separation',
                          default_value=100)
        self.create_input('RenderNodeSocketInt', 'motion_blur_max', 'Max Blur', default_value=32)
        self.create_input('RenderNodeSocketInt', 'motion_blur_steps', 'Steps', default_value=1)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def draw_buttons(self, context, layout):
        layout.prop(self,'motion_blur_position')

    def process(self, context, id, path):
        if not self.process_task(): return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.eevee, key, value)

        self.compare(context.scene.eevee, 'motion_blur_position', self.motion_blur_position)


def register():
    bpy.utils.register_class(RenderNodeSetEeveeMotionBlur)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetEeveeMotionBlur)
