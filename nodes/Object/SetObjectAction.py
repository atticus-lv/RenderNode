import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetObjectAction(RenderNodeBase):
    bl_idname = 'RenderNodeSetObjectAction'
    bl_label = 'Set Object Action'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketObject', 'object', 'Object', show_text=False)
        self.create_input('RenderNodeSocketAction', 'action', 'Action')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        if not self.process_task():return
        ob = self.inputs['object'].get_value()
        action = self.inputs['action'].get_value()
        if ob and action:
            ob.animation_data.action = action


def register():
    bpy.utils.register_class(RenderNodeSetObjectAction)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetObjectAction)
