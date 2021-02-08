import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def poll_camera(self, object):
    return object.type == 'CAMERA'


def update_node(self, context):
    self.update_parms()


class RSNodeCamInputNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeCamInputNode'
    bl_label = 'Camera'

    camera: PointerProperty(name="Camera", type=bpy.types.Object, poll=poll_camera, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketCamera', "Camera")
        self.width = 180

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.prop(self, 'camera', text="")
        if self.camera:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.camera.name

    def get_data(self):
        task_data = {}
        task_data["camera"] = self.camera.name if self.camera else None
        return task_data


def register():
    bpy.utils.register_class(RSNodeCamInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCamInputNode)
