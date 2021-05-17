import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


class RenderNodeSceneCamera(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneCamera'
    bl_label = 'Scene Camera'

    def init(self, context):
        self.create_prop('RenderNodeSocketCamera', "camera", 'Camera')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def process(self):
        self.store_data()
        cam = self.node_dict['camera']

        if cam:
            if cam.type == 'CAMERA':
                self.compare(bpy.context.scene, 'camera', cam)


def register():
    bpy.utils.register_class(RenderNodeSceneCamera)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneCamera)
