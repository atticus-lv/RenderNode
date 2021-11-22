import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

from ...preferences import get_pref

import os
import time
import re


class RenderNodeSetFrameRange(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetFrameRange'
    bl_label = 'Set Scene Frame Range'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketInt', 'frame_start', 'Start')
        self.create_input('RenderNodeSocketInt', 'frame_end', 'End')
        self.create_input('RenderNodeSocketInt', 'frame_step', 'Step')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.inputs['frame_start'].default_value = bpy.context.scene.frame_start
        self.inputs['frame_end'].default_value = bpy.context.scene.frame_end
        self.inputs['frame_step'].default_value = 1

    def draw_buttons(self, context, layout):
        if bpy.data.filepath == '':
            layout.scale_y = 1.25
            layout.label(text='Save your file first', icon='ERROR')

    def process(self, context, id, path):
        if not self.process_task():return

        start = self.inputs['frame_start'].get_value()
        end = self.inputs['frame_end'].get_value()
        if start > end:
            self.inputs['frame_end'].set_value(start)

        if self.inputs['frame_step'].get_value() < 1: self.inputs['frame_step'].set_value(1)

        frame_start = self.inputs['frame_start'].get_value()
        frame_end = self.inputs['frame_end'].get_value()
        frame_step = self.inputs['frame_step'].get_value()

        self.task_dict_append({'frame_start': frame_start,
                               'frame_end': frame_end,
                               'frame_step': frame_step,
                               })


def register():
    bpy.utils.register_class(RenderNodeSetFrameRange)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetFrameRange)
