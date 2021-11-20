import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
import json


class RenderNodeGetTaskInfo(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetTaskInfo'
    bl_label = 'Get Task Info'

    task_info: StringProperty(name='Task Info',default = 'Waiting for task input')

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def draw_buttons(self, context, layout):
        col = layout.box().column(align=True)

        if self.task_info != '':
            for s in self.task_info.split('$$$'):
                col.label(text=s)

    def process(self, context, id, path):
        value = self.process_task()
        if value is None:
            self.task_info = 'No Task Input!'
        data = json.loads(value)
        # set to ui
        self.task_info = '$$$'.join([f"{key.title().replace('_', ' ')}: {value}" for key, value in data.items()])


def register():
    bpy.utils.register_class(RenderNodeGetTaskInfo)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetTaskInfo)
