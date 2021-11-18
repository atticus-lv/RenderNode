import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector
import json


def update_node(self, context):
    self.execute_tree()


class RenderNodeTaskInput(RenderNodeBase):
    bl_idname = 'RenderNodeTaskInput'
    bl_label = 'Task Input'

    def init(self, context):
        self.create_input('RenderNodeSocketString', 'label', 'Label')
        self.create_input('RenderNodeSocketFilePath', 'filepath', 'Path', default_value='//')
        self.create_input('RenderNodeSocketInt', 'frame_start', 'Start')
        self.create_input('RenderNodeSocketInt', 'frame_end', 'End')
        self.create_input('RenderNodeSocketInt', 'frame_step', 'Step')
        self.create_output('RenderNodeSocketTask', 'Task', "Task")
        # capture current frame range
        self.inputs['frame_start'].default_value = bpy.context.scene.frame_start
        self.inputs['frame_end'].default_value = bpy.context.scene.frame_end
        self.inputs['frame_step'].default_value = 1

    def draw_buttons(self, context, layout):
        pass

    def process(self, context, id, path):
        label = self.inputs['label'].get_value()
        p = self.inputs['filepath'].get_value()

        if label:
            self.label = label
        if p:
            self.path = p

        # correct
        start = self.inputs['frame_start'].get_value()
        end = self.inputs['frame_end'].get_value()

        if start > end:
            self.inputs['frame_end'].set_value(start)

        if self.inputs['frame_step'].get_value() < 1: self.inputs['frame_step'].set_value(1)

        frame_start = self.inputs['frame_start'].get_value()
        frame_end = self.inputs['frame_end'].get_value()
        frame_step = self.inputs['frame_step'].get_value()

        self.outputs[0].set_value(json.dumps({'name': self.name,
                                              'label': label,
                                              'filepath': self.path,
                                              'frame_start': frame_start,
                                              'frame_end': frame_end,
                                              'frame_step': frame_step,
                                              }))


def register():
    bpy.utils.register_class(RenderNodeTaskInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeTaskInput)
