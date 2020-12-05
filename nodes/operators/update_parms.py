import bpy
from bpy.props import *
from RenderStackNode.utility import *


class RSN_OT_UpdateParms(bpy.types.Operator):
    """Switch Scene Camera"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    task_name: StringProperty()
    task_data = None

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
        task_name = self.task_name
        self.task_data = nt.get_task_data(task_name)
        # print(self.task_data)

    def send_email(self):
        if 'email' in self.task_data:
            for node_name, email_dict in self.task_data['email'].items():
                try:
                    bpy.ops.rsn.send_email(subject=email_dict['subject'],
                                           content=email_dict['content'],
                                           sender_name=email_dict['sender_name'],
                                           email=email_dict['email'])
                except Exception as e:
                    print(f"RSN ERROR: SMTP Email node > {node_name} < error: {e}")

    def updata_view_layer(self):
        if 'view_layer' in self.task_data:
            bpy.context.window.view_layer = bpy.context.scene.view_layers[self.task_data['view_layer']]

    def updata_scripts(self):
        if 'scripts' in self.task_data:
            for k, value in self.task_data['scripts'].items():
                try:
                    exec(value)
                except Exception as e:
                    print(f"RSN ERROR: scripts node > {k} < error: {e}")
        if 'scripts_file' in self.task_data:
            for node_name, file_name in self.task_data['scripts_file'].items():
                try:
                    c = bpy.data.texts[file_name].as_string()
                    exec(c)
                except Exception as e:
                    print(f"RSN ERROR: scripts node > {node_name} < error: {e}")

    def update_image_format(self):
        if 'color_mode' in self.task_data:
            bpy.context.scene.render.image_settings.color_mode = self.task_data['color_mode']
            bpy.context.scene.render.image_settings.color_depth = self.task_data['color_depth']
            bpy.context.scene.render.image_settings.file_format = self.task_data['file_format']
            bpy.context.scene.render.film_transparent = task_data['transparent']

    def update_frame_range(self):
        if "frame_start" in self.task_data:
            bpy.context.scene.frame_start = self.task_data['frame_start']
            bpy.context.scene.frame_end = self.task_data['frame_end']
            bpy.context.scene.frame_step = self.task_data['frame_step']

    def update_render_engine(self):
        if 'engine' in self.task_data:
            bpy.context.scene.render.engine = self.task_data['engine']
            if 'samples' in self.task_data:
                if self.task_data['engine'] == "BLENDER_EEVEE":
                    bpy.context.scene.eevee.taa_render_samples = self.task_data['samples']
                elif self.task_data['engine'] == "CYCLES":
                    bpy.context.scene.cycles.samples = self.task_data['samples']

    def update_res(self):
        if 'res_x' in self.task_data:
            bpy.context.scene.render.resolution_x = self.task_data['res_x']
            bpy.context.scene.render.resolution_y = self.task_data['res_y']
            bpy.context.scene.render.resolution_percentage = self.task_data['res_scale']

    def update_camera(self):
        if 'camera' in self.task_data:
            cam_name = self.task_data['camera']
            if cam_name:
                bpy.context.scene.camera = bpy.data.objects[cam_name]
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                                break
                        break

    def execute(self, context):
        self.get_data()
        self.update_camera()
        self.update_res()
        self.update_render_engine()
        self.update_frame_range()
        self.updata_scripts()
        self.updata_view_layer()
        self.send_email()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)


def unregister():
    bpy.utils.unregister_class(RSN_OT_UpdateParms)
