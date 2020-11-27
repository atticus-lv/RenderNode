import json
import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

class RSN_OT_UpdateParms(bpy.types.Operator):
    """Switch Scene Camera"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    cam_name: StringProperty(name="Camera name")
    def update_camera(self):
        try:
            context.scene.camera = bpy.data.objects[self.cam_name]
            context.area.spaces[0].region_3d.view_perspective = 'CAMERA'
        except(Exception):
            self.report({"WARNING"}, f"Camera {self.CamName} not found")

    def execute(self, context):
        self.update_camera()

        return {'FINISHED'}

class RSNodeSocketViewerNode(RenderStackNode):
    bl_idname = 'RSNodeRenderViewerNode'
    bl_label = 'Viewer'

    def init(self, context):
        self.inputs.new('NodeSocketString', "Info")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        pass

def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)
    bpy.utils.register_class(RSNodeSocketViewerNode)