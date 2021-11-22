import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetObjectLocation(RenderNodeBase):
    bl_idname = 'RenderNodeSetObjectLocation'
    bl_label = 'Set Object Location'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketObject', 'object', 'Object', show_text=False)
        self.create_input('RenderNodeSocketTranslation', 'location', 'Location')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        if not self.process_task():return
        ob = self.inputs['object'].get_value()
        location = self.inputs['location'].get_value()
        if ob and location:
            ob.location = location


def register():
    bpy.utils.register_class(RenderNodeSetObjectLocation)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetObjectLocation)
