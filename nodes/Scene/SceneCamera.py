import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSceneCamera(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneCamera'
    bl_label = 'Scene Camera'

    def init(self, context):
        self.create_prop('RenderNodeSocketCamera', "camera", 'Camera')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def process(self):
        self.store_data()

        cam = self.node_dict['camera']
        if cam: self.compare(bpy.context.scene, 'camera', cam)



def register():
    bpy.utils.register_class(RenderNodeSceneCamera)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneCamera)
