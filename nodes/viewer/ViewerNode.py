import json
import bpy
from bpy.props import *

from RenderStackNode.node_tree import RenderStackNode
from RenderStackNode.core.get_tree_info import NODE_TREE


class RSN_OT_UpdateParms(bpy.types.Operator):
    """Switch Scene Camera"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    cam_name: StringProperty(name="Camera name")

    engine = None
    samples = None

    res_x = None
    res_y = None
    res_scale = None

    def get_data(self):
        nt = NODE_TREE(bpy.context.space_data.edit_tree)
        for name in nt.dict[nt.nt.nodes.active.inputs[0].links[0].from_node.name]:
            node = nt.nt.nodes[name]

            if node.bl_idname == "RSNodeCamInputNode":
                self.cam_name = node.camera.name

            elif node.bl_idname == "ResolutionInputNode":
                self.res_x = node.res_x
                self.res_y = node.res_y
                self.res_scale = node.res_scale

            elif node.bl_idname == "RSNodeCyclesRenderSettingsNode":
                self.engine = "CYCLES"
                self.samples = node.inputs["Samples"].default_value

            elif node.bl_idname == "RSNodeEeveeRenderSettingsNode":
                self.engine = "BLENDER_EEVEE"
                self.samples = node.inputs["Samples"].default_value

    def update_render_engine(self):
        if self.engine:
            bpy.context.scene.render.engine = self.engine
            if self.samples:
                if self.engine == "BLENDER_EEVEE":
                    bpy.context.scene.eevee.taa_render_samples = self.samples
                elif self.engine == "CYCLES":
                    bpy.context.scene.cycles.samples = self.samples

    def update_res(self):
        if self.res_x:
            bpy.context.scene.render.resolution_x = self.res_x
        if self.res_y:
            bpy.context.scene.render.resolution_y = self.res_y
        if self.res_scale:
            bpy.context.scene.render.resolution_percentage = self.res_scale

        self.res_x = None
        self.res_y = None
        self.res_scale = None

    def update_camera(self):
        try:
            if not bpy.context.scene.camera.name == self.cam_name:
                bpy.context.scene.camera = bpy.data.objects[self.cam_name]
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                        break
                    break
        except(Exception) as e:
            # self.report({"ERROR"}, f"No Camera {self.cam_name}")
            self.report({"WARNING"}, f"{e}")
        finally:
            self.cam_name = ""

    def execute(self, context):
        self.get_data()
        self.update_camera()
        self.update_res()
        self.update_render_engine()

        return {'FINISHED'}


class RSNodeSocketViewerNode(RenderStackNode):
    bl_idname = 'RSNodeRenderViewerNode'
    bl_label = 'Viewer'

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.operator("rsn.update_parms")


def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)
    bpy.utils.register_class(RSNodeSocketViewerNode)


def unregister():
    bpy.utils.unregister_class(RSN_OT_UpdateParms)
    bpy.utils.unregister_class(RSNodeSocketViewerNode)
