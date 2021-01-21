import bpy
from bpy.props import StringProperty, BoolProperty
from RenderStackNode.utility import *

import logging
import time
import os

LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


class RSN_OT_UpdateParms(bpy.types.Operator):
    """Switch Scene Camera"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    use_render_mode: BoolProperty(default=True, description="Prevent from python context error")

    view_mode_handler: StringProperty()
    update_scripts: BoolProperty(default=False)

    nt: None
    task_data = None

    def reroute(self, node):
        def is_task_node(node):
            if node.bl_idname == "RSNodeTaskNode":
                return node.name

            sub_node = node.inputs[0].links[0].from_node

            return is_task_node(sub_node)

        task_node_name = is_task_node(node)
        return task_node_name

    def warning_node_color(self, node_name):
        self.nt.nodes[node_name].use_custom_color = 1
        self.nt.nodes[node_name].color = (1, 0, 0)

    def get_data(self):
        if not self.use_render_mode:
            rsn_tree = RSN_NodeTree()
            self.nt = rsn_tree.get_context_tree()
        else:
            rsn_tree = RSN_NodeTree()
            self.nt = rsn_tree.get_wm_node_tree()

        rsn_task = RSN_Task(node_tree=self.nt,
                            root_node_name=self.view_mode_handler)
        node_list_dict = rsn_task.get_sub_node_from_task(task_name=self.view_mode_handler,
                                                         return_dict=True)
        if node_list_dict:
            self.task_data = rsn_task.get_task_data(task_name=self.view_mode_handler,
                                                    task_dict=node_list_dict)
        if self.task_data:
            logger.debug(f'Get >{self.view_mode_handler}< data')
        else:
            logger.debug(f'Not task is linked to the viewer')

    def update_ev(self):
        if 'ev' in self.task_data:
            if bpy.context.scene.view_settings.exposure != self.task_data['ev']:
                bpy.context.scene.view_settings.exposure = self.task_data['ev']
            if bpy.context.scene.view_settings.view_transform != self.task_data['view_transform']:
                bpy.context.scene.view_settings.view_transform = self.task_data['view_transform']
            if bpy.context.scene.view_settings.look != self.task_data['look']:
                try:
                    bpy.context.scene.view_settings.look = self.task_data['look']
                except:
                    pass
            if bpy.context.scene.view_settings.gamma != self.task_data['gamma']:
                bpy.context.scene.view_settings.gamma = self.task_data['gamma']

    def update_path(self):
        dir = self.make_path()
        postfix = self.get_postfix()
        if bpy.context.scene.render.use_file_extension != 1:
            bpy.context.scene.render.use_file_extension = 1

        if bpy.context.scene.render.filepath != os.path.join(dir, postfix):
            bpy.context.scene.render.filepath = os.path.join(dir, postfix)

    def make_path(self):
        task = self.task_data
        if 'path' in task and task['path'] != '':
            if not task['use_blend_file_path']:
                directory_path = os.path.dirname(task['path'])
            else:
                directory_path = os.path.dirname(bpy.data.filepath)
            try:
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                return directory_path

            except(Exception) as e:
                self.report({'ERROR'}, f'File Path: No Such a Path')
                print(directory_path, e)
        else:
            return os.path.dirname(bpy.data.filepath) + "\\"

    def get_postfix(self):
        scn = bpy.context.scene
        cam = scn.camera
        pref = bpy.context.preferences.addons.get('RenderStackNode').preferences
        separator = pref.file_path_separator

        postfix = ""
        date_now = str(time.strftime("%m-%d", time.localtime()))
        time_now = str(time.strftime("%H_%M", time.localtime()))

        if 'path_format' in self.task_data:
            shot_export_name = self.task_data["path_format"]
            for string in shot_export_name.split("/"):
                for r in string.split('$'):
                    if r.startswith("date"):
                        postfix += date_now + separator
                    elif r.startswith("time"):
                        postfix += time_now + separator
                    elif r.startswith("camera"):
                        postfix += cam.name + separator
                    elif r.startswith("engine"):
                        postfix += bpy.context.scene.render.engine + separator
                    elif r.startswith("res"):
                        postfix += f"{scn.render.resolution_x}x{scn.render.resolution_y}" + separator
                    elif r.startswith("ev"):
                        postfix += scn.view_settings.exposure + separator
                    elif r.startswith("label"):
                        postfix += self.task_data["label"] + separator
                    elif r.startswith("vl"):
                        postfix += bpy.context.view_layer.name + separator
                    elif r.startswith("blend"):
                        try:
                            blend_name = bpy.path.basename(bpy.data.filepath)[:-6]
                            r.replace("blend", blend_name)
                            postfix += r + separator
                        except Exception as e:
                            pass
                    else:
                        postfix += r

                if postfix.endswith(separator): postfix = postfix[:-1]
                postfix += "/"

            if postfix.endswith("/"): postfix = postfix[:-1]
        return postfix

    def update_view_layer_passes(self):
        if 'view_layer_passes' in self.task_data:
            for node_name, dict in self.task_data['view_layer_passes'].items():
                try:
                    bpy.ops.rsn.creat_compositor_node(
                        view_layer=self.task_data['view_layer_passes'][node_name]['view_layer'],
                        use_passes=self.task_data['view_layer_passes'][node_name]['use_passes'])
                except Exception as e:
                    logger.warning(f'View Layer Passes {node_name} error', exc_info=e)
        else:
            bpy.ops.rsn.creat_compositor_node(use_passes=0, view_layer=bpy.context.window.view_layer.name)

    def update_object_psr(self):
        if 'object_psr' in self.task_data:
            for node_name, dict in self.task_data['object_psr'].items():
                try:
                    ob = bpy.data.objects[dict['object']]
                except:
                    ob = None
                if ob:
                    if ob.location != dict['location'] and dict['use_p']:
                        ob.location = dict['location']
                    if ob.scale != dict['scale'] and dict['use_s']:
                        ob.scale = dict['scale']
                    if ob.rotation_euler != dict['rotation'] and dict['use_r']:
                        ob.rotation_euler = dict['rotation']

    def update_object_material(self):
        if 'object_material' in self.task_data:
            for node_name, dict in self.task_data['object_material'].items():
                try:
                    ob = bpy.data.objects[dict['object']]
                except:
                    ob = None
                if ob:
                    try:
                        if ob.material_slots[dict['slot_index']].material.name != dict['new_material']:
                            ob.material_slots[dict['slot_index']].material = bpy.data.materials[dict['new_material']]
                    except Exception as e:
                        pass

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
                logger.warning(f'SSM LightStudio node error', exc_info=e)

    def send_email(self):
        if 'email' in self.task_data:
            for node_name, email_dict in self.task_data['email'].items():
                try:
                    bpy.ops.rsn.send_email(subject=email_dict['subject'],
                                           content=email_dict['content'],
                                           sender_name=email_dict['sender_name'],
                                           email=email_dict['email'])
                except Exception as e:
                    logger.warning(f'SMTP Email {node_name} error', exc_info=e)
                    self.warning_node_color(node_name)

    def updata_view_layer(self):
        if 'view_layer' in self.task_data and bpy.context.window.view_layer.name != self.task_data['view_layer']:
            bpy.context.window.view_layer = bpy.context.scene.view_layers[self.task_data['view_layer']]

    def updata_scripts(self):
        if 'scripts' in self.task_data:
            for node_name, value in self.task_data['scripts'].items():
                try:
                    exec(value)
                except Exception as e:
                    logger.warning(f'Scripts node {node_name} error', exc_info=e)
                    self.warning_node_color(node_name)

        if 'scripts_file' in self.task_data:
            for node_name, file_name in self.task_data['scripts_file'].items():
                try:
                    c = bpy.data.texts[file_name].as_string()
                    exec(c)
                except Exception as e:
                    print(f"RSN ERROR: scripts node > {node_name} < error: {e}")
                    logger.warning(f'scripts node {node_name} error', exc_info=e)
                    self.warning_node_color(node_name)

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
                if bpy.context.scene.luxcore.halt.use_samples != True:
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
        pref = bpy.context.preferences.addons.get('RenderStackNode').preferences
        logger.setLevel(int(pref.log_level))
        logger.debug('update parms op START')
        self.get_data()
        if self.task_data:
            self.update_camera()
            self.update_ev()
            self.update_res()
            self.update_render_engine()

            self.update_object_material()
            self.update_object_psr()

            self.update_frame_range()
            self.updata_view_layer()

            self.update_image_format()
            self.update_slots()

            self.update_world()
            self.ssm_light_studio()
            if pref.node_viewer.update_scripts or self.use_render_mode:
                self.updata_scripts()
            if pref.node_viewer.update_path or self.use_render_mode:
                self.update_path()
            if pref.node_viewer.update_view_layer_passes or self.use_render_mode:
                self.update_view_layer_passes()
            if self.use_render_mode:
                self.send_email()

        logger.debug('update parms op FINISHED')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)


def unregister():
    bpy.utils.unregister_class(RSN_OT_UpdateParms)
