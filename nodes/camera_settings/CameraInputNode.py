import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def poll_camera(self, object):
    return object.type == 'CAMERA'


class RSNodeCamInputNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCamInputNode'
    bl_label = 'Camera'

    camera: PointerProperty(name="Camera", type=bpy.types.Object, poll=poll_camera)

    def init(self, context):
        self.outputs.new('RSNodeSocketCamera', "Camera")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'camera', text="")

    def process(self):
        dict = {}
        if self.camera:
            dict["name"] = self.camera.name
        else:
            dict["name"] = None
        self.outputs["Camera"]["Camera"] = dict


def register():
    bpy.utils.register_class(RSNodeCamInputNode)

def unregister():
    bpy.utils.unregister_class(RSNodeCamInputNode)