import bpy
from bpy.props import StringProperty, BoolProperty
from RenderStackNode.utility import *


class RSN_OT_UpdateParms(bpy.types.Operator):
    """Switch Scene Camera"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    viewer_handler: StringProperty()
    update_scripts: BoolProperty(default=False)

    nt: None
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
        if self.viewer_handler != '':
            nt = NODE_TREE(bpy.context.space_data.edit_tree, node_name=self.viewer_handler)
        else:
            nt = NODE_TREE(bpy.context.space_data.edit_tree)
        self.nt = nt
        task_name = self.task_name
        try:
            self.task_data = nt.get_task_data(task_name)
            return True
        except KeyError:
            return None

    def update_slots(self):
        if 'render_slot' in self.task_data:
            if bpy.data.images['Render Result'].render_slots.active_index != self.task_data['render_slot']:
                bpy.data.images['Render Result'].render_slots.active_index = self.task_data['render_slot']

    def update_world(self):
        if 'world' in self.task_data:
            if bpy.context.scene.world.name != self.task_data['world']:
                bpy.context.scene.world = bpy.data.worlds[self.task_data['world']]

    def ssm_light_studio(self):
        if 'ssm_light_studio' in self.task_data:
            index = self.task_data['ssm_light_studio']
            try:
                if bpy.context.scene.ssm.light_studio_index != index:
                    bpy.context.scene.ssm.light_studio_index = index
            except Exception as e:
                print(f"RSN ERROR: SSM LightStudio node error: {e}")

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
                    self.nt.node[node_name].use_custom_color = 1
                    self.nt.node[node_name].color = (1, 0, 0)

    def updata_view_layer(self):
        if 'view_layer' in self.task_data and bpy.context.window.view_layer.name != self.task_data['view_layer']:
            bpy.context.window.view_layer = bpy.context.scene.view_layers[self.task_data['view_layer']]

    def updata_scripts(self):
        if 'scripts' in self.task_data:
            for k, value in self.task_data['scripts'].items():
                try:
                    exec(value)
                except Exception as e:
                    print(f"RSN ERROR: scripts node > {k} < error: {e}")
                    self.nt.node[k].use_custom_color = 1
                    self.nt.node[k].color = (1, 0, 0)

        if 'scripts_file' in self.task_data:
            for node_name, file_name in self.task_data['scripts_file'].items():
                try:
                    c = bpy.data.texts[file_name].as_string()
                    exec(c)
                except Exception as e:
                    print(f"RSN ERROR: scripts node > {node_name} < error: {e}")
                    self.nt.node[node_name].use_custom_color = 1
                    self.nt.node[node_name].color = (1, 0, 0)

    def update_image_format(self):
        if 'color_mode' in self.task_data:
            if bpy.context.scene.render.image_settings.color_mode != self.task_data['color_mode']:
                bpy.context.scene.render.image_settings.color_mode = self.task_data['color_mode']
            if bpy.context.scene.render.image_settings.color_depth != self.task_data['color_depth']:
                bpy.context.scene.render.image_settings.color_depth = self.task_data['color_depth']
            if bpy.context.scene.render.image_settings.file_format != self.task_data['file_format']:
                bpy.context.scene.render.image_settings.file_format = self.task_data['file_format']
            if bpy.context.scene.render.film_transparent != self.task_data['transparent']:
                bpy.context.scene.render.film_transparent = self.task_data['transparent']

    def update_frame_range(self):
        if "frame_start" in self.task_data:
            if bpy.context.scene.frame_start != self.task_data['frame_start']:
                bpy.context.scene.frame_start = self.task_data['frame_start']
            if bpy.context.scene.frame_end != self.task_data['frame_end']:
                bpy.context.scene.frame_end = self.task_data['frame_end']
            if bpy.context.scene.frame_step != self.task_data['frame_step']:
                bpy.context.scene.frame_step = self.task_data['frame_step']

    def update_render_engine(self):
        if 'engine' in self.task_data and bpy.context.scene.render.engine != self.task_data['engine']:
            if True in (self.task_data['engine'] == 'LUXCORE' and 'BlendLuxCore' in bpy.context.preferences.addons,
                        self.task_data['engine'] != 'LUXCORE'):
                bpy.context.scene.render.engine = self.task_data['engine']

        if 'samples' in self.task_data:
            if self.task_data['engine'] == "BLENDER_EEVEE":
                if bpy.context.scene.eevee.taa_render_samples != self.task_data['samples']:
                    bpy.context.scene.eevee.taa_render_samples = self.task_data['samples']
            elif self.task_data['engine'] == "CYCLES":
                if bpy.context.scene.cycles.samples != self.task_data['samples']:
                    bpy.context.scene.cycles.samples = self.task_data['samples']

        if 'luxcore_half' in self.task_data:
            if bpy.context.scene.luxcore.halt.enable != True:
                bpy.context.scene.luxcore.halt.enable = True

            if self.task_data['luxcore_half']['use_samples'] is False and self.task_data['luxcore_half'][
                'use_time'] is False:
                bpy.context.scene.luxcore.halt.use_samples = True

            elif self.task_data['luxcore_half']['use_samples'] is True and self.task_data['luxcore_half'][
                'use_time'] is False:
                if bpy.context.scene.luxcore.halt.use_samples !=True:
                    bpy.context.scene.luxcore.halt.use_samples = True
                if bpy.context.scene.luxcore.halt.use_time != False:
                    bpy.context.scene.luxcore.halt.use_time = False
                if bpy.context.scene.luxcore.halt.samples != self.task_data['luxcore_half']['samples']:
                    bpy.context.scene.luxcore.halt.samples = self.task_data['luxcore_half']['samples']

            elif self.task_data['luxcore_half']['use_samples'] is False and self.task_data['luxcore_half'][
                'use_time'] is True:
                if bpy.context.scene.luxcore.halt.use_samples != False:
                    bpy.context.scene.luxcore.halt.use_samples = False
                if bpy.context.scene.luxcore.halt.use_time != True:
                    bpy.context.scene.luxcore.halt.use_time = True
                if bpy.context.scene.luxcore.halt.time != self.task_data['luxcore_half']['time']:
                    bpy.context.scene.luxcore.halt.time = self.task_data['luxcore_half']['time']

    def update_res(self):
        if 'res_x' in self.task_data:
            if bpy.context.scene.render.resolution_x != self.task_data['res_x']:
                bpy.context.scene.render.resolution_x = self.task_data['res_x']
            if bpy.context.scene.render.resolution_y != self.task_data['res_y']:
                bpy.context.scene.render.resolution_y = self.task_data['res_y']
            if bpy.context.scene.render.resolution_percentage != self.task_data['res_scale']:
                bpy.context.scene.render.resolution_percentage = self.task_data['res_scale']

    def update_camera(self):
        if 'camera' in self.task_data:
            cam_name = self.task_data['camera']
            if cam_name and bpy.context.scene.camera and bpy.context.scene.camera.name != cam_name:
                bpy.context.scene.camera = bpy.data.objects[cam_name]
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                                break
                        break

    def execute(self, context):
        if self.get_data():
            self.update_camera()
            self.update_res()
            self.update_render_engine()
            self.update_frame_range()
            self.updata_view_layer()
            self.update_image_format()
            self.update_slots()
            self.update_world()
            self.ssm_light_studio()
            if not self.update_scripts:
                self.updata_scripts()
            if not context.window_manager.rsn_viewer_modal:
                self.send_email()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)


def unregister():
    bpy.utils.unregister_class(RSN_OT_UpdateParms)
