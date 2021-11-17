import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetSceneCamera(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneCamera'
    bl_label = 'Set Scene Camera'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_input('RenderNodeSocketCamera', "camera", 'Camera')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        task = self.inputs[0].get_value()
        cam = self.inputs[1].get_value()

        if cam and task: self.compare(bpy.context.scene, 'camera', cam)


def register():
    bpy.utils.register_class(RenderNodeSetSceneCamera)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetSceneCamera)
