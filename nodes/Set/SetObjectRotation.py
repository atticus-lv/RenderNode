import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetObjectRotation(RenderNodeBase):
    bl_idname = 'RenderNodeSetObjectRotation'
    bl_label = 'Set Object Rotation'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketObject', 'object', 'Object', show_text=False)
        self.create_input('RenderNodeSocketEuler', 'rotate', 'Rotation')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        self.process_task()
        ob = self.inputs['object'].get_value()
        rotate = self.inputs['rotate'].get_value()
        if ob and rotate:
            ob.rotation_euler = rotate


def register():
    bpy.utils.register_class(RenderNodeSetObjectRotation)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetObjectRotation)
