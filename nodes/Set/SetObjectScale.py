import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetObjectScale(RenderNodeBase):
    bl_idname = 'RenderNodeSetObjectScale'
    bl_label = 'Set Object Scale'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketObject', 'object', 'Object', show_text=False)
        self.create_input('RenderNodeSocketXYZ', 'scale', 'Scale',default_value=[1,1,1])

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        self.process_task()
        ob = self.inputs['object'].get_value()
        scale = self.inputs['scale'].get_value()
        if ob and scale:
            ob.scale = scale


def register():
    bpy.utils.register_class(RenderNodeSetObjectScale)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetObjectScale)
