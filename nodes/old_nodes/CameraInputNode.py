import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def poll_camera(self, object):
    return object.type == 'CAMERA'


def update_node(self, context):
    self.update_parms()


class RSNodeCamInputNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodeCamInputNode'
    bl_label = 'Camera'

    camera: PointerProperty(name="Camera", type=bpy.types.Object, poll=poll_camera, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketCamera', "Camera")
        self.width = 180
        # inherit the Scene camera\
        try:
            if context.scene.camera: self.camera = context.scene.camera
        except:
            pass

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.prop(self, 'camera', text="")
        if self.camera:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.camera.name

    def get_data(self):
        if self.camera:
            task_data = {}
            task_data["camera"] = f"bpy.data.objects['{self.camera.name}']"
            return task_data


def register():
    bpy.utils.register_class(RSNodeCamInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCamInputNode)
