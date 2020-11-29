import bpy
from bpy.props import *

from RenderStackNode.core.get_tree_info import NODE_TREE


class RSN_OT_UpdateParms(bpy.types.Operator):
    """Switch Scene Camera"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    index: IntProperty(default=0, min=0)

    cam_name: StringProperty(name="Camera name")

    engine = None
    samples = None

    res_x = None
    res_y = None
    res_scale = None

    frame_start = None
    frame_end = None
    frame_step = None

    def reroute(self, node):
        def is_task_node(node):
            if node.bl_idname == "RSNodeTaskNode":
                print(f">> get task node {node.name}")
                return node.name

            sub_node = node.inputs[0].links[0].from_node

            return is_task_node(sub_node)

        task_node_name = is_task_node(node)
        return task_node_name

    def get_data(self):
        nt = NODE_TREE(bpy.context.space_data.edit_tree)
        task_name = self.reroute(nt.nt.nodes.active.inputs[self.index].links[0].from_node)

        for node_name in nt.dict[task_name]:
            node = nt.nt.nodes[node_name]

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

            elif node.bl_idname == "FrameRangeInputNode":
                if node.frame_end < node.frame_start:
                    node.frame_end = node.frame_start
                self.frame_start = node.frame_start
                self.frame_end = node.frame_end
                self.frame_step = node.frame_step

    def update_frame_range(self):
        if self.frame_start:
            bpy.context.scene.frame_start = self.frame_start
            bpy.context.scene.frame_end = self.frame_end
            bpy.context.scene.frame_step = self.frame_step

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
        except(Exception):
            pass
        finally:
            self.cam_name = ""

    def execute(self, context):
        self.get_data()
        self.update_camera()
        self.update_res()
        self.update_render_engine()
        self.update_frame_range()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)


def unregister():
    bpy.utils.unregister_class(RSN_OT_UpdateParms)
