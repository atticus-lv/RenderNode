import bpy
from bpy.props import StringProperty, BoolProperty
from ..utility import *
from ..preferences import get_pref

import logging
import time
import os
from functools import wraps
import re

# init logger
LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


# get the update time
def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        s = f'{(t2 - t1) * 1000: .4f} ms'
        bpy.context.window_manager.rsn_tree_time = s
        logger.info(f"RSN Tree: update took{s}\n")
        return result

    return measure_time


def compare(obj: object, attr: str, val):
    """Use for compare and apply attribute since some properties change may cause depsgraph changes"""
    try:
        if getattr(obj, attr) != val:
            setattr(obj, attr, val)
            logger.debug(f'Attribute "{attr}" SET “{val}”')
    except AttributeError as e:
        logger.info(e)


class RSN_OT_UpdateParms(bpy.types.Operator):
    """Update RSN parameters"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    use_render_mode: BoolProperty(default=True, description="Prevent from python context error")

    view_mode_handler: StringProperty()
    update_scripts: BoolProperty(default=False)

    nt: None
    task_data = None

    def execute(self, context):
        """update_parm method"""
        self.data_changes()
        return {'FINISHED'}

    def reroute(self, node):
        """help to ignore the reroute node"""

        def is_task_node(node):
            """return the task_node only"""
            if node.bl_idname == "RSNodeTaskNode":
                return node.name

            sub_node = node.inputs[0].links[0].from_node

            return is_task_node(sub_node)

        task_node_name = is_task_node(node)
        return task_node_name

    def warning_node_color(self, node_name):
        try:
            self.nt.nodes[node_name].set_warning()
        except Exception:
            pass

    # first get task data
    def get_data(self):
        """Viewer mode and render mode.Prevent the python state error"""

        if not self.use_render_mode:
            # read the node tree from context space_data
            rsn_tree = RSN_NodeTree()
            self.nt = rsn_tree.get_context_tree()
        else:
            # read the node tree from window_manager
            rsn_tree = RSN_NodeTree()
            self.nt = rsn_tree.get_wm_node_tree()

        rsn_task = RSN_Nodes(node_tree=self.nt,
                             root_node_name=self.view_mode_handler)
        # get the task node and the sub node, return dict
        node_list_dict = rsn_task.get_children_from_task(task_name=self.view_mode_handler,
                                                         return_dict=True)
        # if the task have sub node, get the data of them
        if node_list_dict:
            self.task_data = rsn_task.get_task_data(task_name=self.view_mode_handler,
                                                    task_dict=node_list_dict)
        if self.task_data:
            logger.debug(f'Get Task "{self.view_mode_handler}"')
        else:
            logger.debug(f'Not task is linked to the viewer')

    def update_color_management(self):
        """may change in 2.93 version"""
        if 'ev' in self.task_data:
            vs = bpy.context.scene.view_settings
            compare(vs, 'exposure', self.task_data['ev'])
            compare(vs, 'gamma', self.task_data['gamma'])
            try:
                compare(vs, 'view_transform', self.task_data['view_transform'])
                compare(vs, 'look', self.task_data['look'])
            except:  # ocio change in 2.93
                pass

    def update_path(self):
        dir = self.make_path()
        postfix = self.get_postfix()

        rn = bpy.context.scene.render

        compare(rn, 'use_file_extension', 1)
        compare(rn, 'filepath', os.path.join(dir, postfix))

    def make_path(self):
        """only save files will work"""
        task = self.task_data
        if 'path' in task:
            if task['path'] != '':
                directory_path = os.path.dirname(task['path'])
                try:
                    if not os.path.exists(directory_path):
                        os.makedirs(directory_path)
                    return directory_path
                except Exception as e:
                    self.report({'ERROR'}, f'File Path: No Such a Path')
        else:
            return os.path.dirname(bpy.data.filepath) + "/"

    def get_postfix(self):
        """path expression"""
        scn = bpy.context.scene
        cam = scn.camera

        blend_name = ''
        postfix = ''

        date_now = str(time.strftime("%m-%d", time.localtime()))
        time_now = str(time.strftime("%H-%M", time.localtime()))

        if 'path' in self.task_data:

            shot_export_name = self.task_data["path_format"]
            # replace time
            postfix = shot_export_name.replace('$date', date_now)
            postfix = postfix.replace('$time', time_now)
            # replace camera name
            if cam:
                postfix = postfix.replace('$camera', cam.name)
            else:
                postfix = postfix
            # replace engine
            postfix = postfix.replace('$engine', bpy.context.scene.render.engine)
            # replace res
            postfix = postfix.replace('res', f"{scn.render.resolution_x}x{scn.render.resolution_y}")
            # replace label
            postfix = postfix.replace('$label', self.task_data["label"])
            # replace view_layer
            postfix = postfix.replace('$vl', bpy.context.view_layer.name)

            # frame completion
            STYLE = re.search(r'([$]F\d)', postfix)
            if STYLE:
                c_frame = bpy.context.scene.frame_current
                format = f'0{STYLE.group(0)[-1:]}d'
                postfix = postfix.replace(STYLE.group(0), f'{c_frame:{format}}')

            # replace filename
            try:
                blend_name = bpy.path.basename(bpy.data.filepath)[:-6]
                postfix = postfix.replace('$blend', blend_name)
            except Exception:
                return 'untitled'

        return postfix

    def update_view_layer_passes(self):
        """each view layer will get a file output node
        but I recommend to save an Multilayer exr file instead of use this node
        """
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

    def update_object_display(self):
        if 'object_display' in self.task_data:
            for node_name, dict in self.task_data['object_display'].items():
                try:
                    ob = bpy.data.objects[dict['object']]
                except:
                    ob = None
                if ob:
                    compare(ob, 'hide_viewport', dict['hide_viewport'])
                    compare(ob, 'hide_render', dict['hide_render'])

    def update_object_psr(self):
        if 'object_psr' in self.task_data:
            for node_name, dict in self.task_data['object_psr'].items():
                try:
                    ob = bpy.data.objects[dict['object']]
                except:
                    ob = None
                if ob:
                    if 'location' in dict:
                        compare(ob, 'location', dict['location'])
                    if 'scale' in dict:
                        compare(ob, 'scale', dict['scale'])
                    if 'rotation' in dict:
                        compare(ob, 'rotation_euler', dict['rotation'])

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

    def update_object_data(self):
        if 'object_data' in self.task_data:
            for node_name, dict in self.task_data['object_data'].items():
                try:
                    ob = bpy.data.objects[dict['object']]
                except:
                    ob = None
                if ob:
                    value = dict['value']
                    obj, attr = source_attr(ob.data, dict['data_path'])
                    compare(obj, attr, value)

    def update_object_modifier(self):
        if 'object_modifier' in self.task_data:
            for node_name, dict in self.task_data['object_modifier'].items():
                try:
                    ob = bpy.data.objects[dict['object']]
                except:
                    ob = None
                if ob:
                    value = dict['value']
                    match = re.match(r"modifiers[[](.*?)[]]", dict['data_path'])
                    name = match.group(1)
                    if name:
                        data_path = dict['data_path'].split('.')[-1]
                        modifier = ob.modifiers[name[1:-1]]
                        compare(modifier, data_path, value)

    def update_slots(self):
        if 'render_slot' in self.task_data:
            compare(bpy.data.images['Render Result'].render_slots, 'active_index', self.task_data['render_slot'])

    def update_world(self):
        if 'world' in self.task_data:
            if bpy.context.scene.world.name != self.task_data['world']:
                bpy.context.scene.world = bpy.data.worlds[self.task_data['world']]

    def ssm_light_studio(self):
        if 'ssm_light_studio' in self.task_data:
            index = self.task_data['ssm_light_studio']
            try:
                compare(bpy.context.scene.ssm, 'light_studio_index', index)
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
        if 'image_settings' in self.task_data:
            rn = bpy.context.scene.render
            image_settings = self.task_data['image_settings']
            compare(rn.image_settings, 'file_format', image_settings['file_format'])
            compare(rn.image_settings, 'color_mode', image_settings['color_mode'])
            compare(rn.image_settings, 'color_depth', image_settings['color_depth'])
            compare(rn.image_settings, 'use_preview', image_settings['use_preview'])
            compare(rn.image_settings, 'compression', image_settings['compression'])
            compare(rn.image_settings, 'quality', image_settings['quality'])
            compare(rn, 'film_transparent', image_settings['transparent'])

    def update_frame_range(self):
        if "frame_start" in self.task_data:
            scn = bpy.context.scene
            compare(scn, 'frame_start', self.task_data['frame_start'])
            compare(scn, 'frame_end', self.task_data['frame_end'])
            compare(scn, 'frame_step', self.task_data['frame_step'])

    def update_render_engine(self):
        # engine settings
        if 'engine' in self.task_data:
            if self.task_data['engine'] in {'CYCLES', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}:
                compare(bpy.context.scene.render, 'engine', self.task_data['engine'])
            elif self.task_data['engine'] == 'octane':
                compare(bpy.context.scene.render, 'engine', self.task_data['engine'])
            elif self.task_data['engine'] == 'LUXCORE':
                compare(bpy.context.scene.render, 'engine', self.task_data['engine'])
        # samples
        if 'samples' in self.task_data:
            if self.task_data['engine'] == "BLENDER_EEVEE":
                compare(bpy.context.scene.eevee, 'taa_render_samples', self.task_data['samples'])
            elif self.task_data['engine'] == "CYCLES":
                compare(bpy.context.scene.cycles, 'samples', self.task_data['samples'])
        # luxcore
        if 'luxcore_half' in self.task_data and 'BlendLuxCore' in bpy.context.preferences.addons:
            if not bpy.context.scene.luxcore.halt.enable:
                bpy.context.scene.luxcore.halt.enable = True

            if self.task_data['luxcore_half']['use_samples'] is False and self.task_data['luxcore_half'][
                'use_time'] is False:
                bpy.context.scene.luxcore.halt.use_samples = True

            elif self.task_data['luxcore_half']['use_samples'] is True and self.task_data['luxcore_half'][
                'use_time'] is False:
                if not bpy.context.scene.luxcore.halt.use_samples:
                    bpy.context.scene.luxcore.halt.use_samples = True
                if bpy.context.scene.luxcore.halt.use_time:
                    bpy.context.scene.luxcore.halt.use_time = False

                compare(bpy.context.scene.luxcore.halt, 'samples', self.task_data['luxcore_half']['samples'])

            elif self.task_data['luxcore_half']['use_samples'] is False and self.task_data['luxcore_half'][
                'use_time'] is True:
                if bpy.context.scene.luxcore.halt.use_samples:
                    bpy.context.scene.luxcore.halt.use_samples = False
                if not bpy.context.scene.luxcore.halt.use_time:
                    bpy.context.scene.luxcore.halt.use_time = True

                compare(bpy.context.scene.luxcore.halt, 'time', self.task_data['luxcore_half']['time'])
        # octane
        elif 'octane' in self.task_data and 'octane' in bpy.context.preferences.addons:
            for key, value in self.task_data['octane'].items():
                compare(bpy.context.scene.octane, key, value)
        # CYCLES
        if 'cycles_light_path' in self.task_data:
            for key, value in self.task_data['cycles_light_path'].items():
                compare(bpy.context.scene.cycles, key, value)

    def update_res(self):
        if 'res_x' in self.task_data:
            rn = bpy.context.scene.render
            compare(rn, 'resolution_x', self.task_data['res_x'])
            compare(rn, 'resolution_y', self.task_data['res_y'])
            compare(rn, 'resolution_percentage', self.task_data['res_scale'])

    def update_camera(self):
        if 'camera' in self.task_data and self.task_data['camera']:
            cam = bpy.data.objects[self.task_data['camera']]
            compare(bpy.context.scene, 'camera', cam)

    @timefn
    def data_changes(self):
        pref = get_pref()
        logger.setLevel(int(pref.log_level))

        self.get_data()

        if self.task_data:
            self.update_camera()
            self.update_color_management()
            self.update_res()
            self.update_render_engine()

            self.update_object_display()
            self.update_object_psr()
            self.update_object_data()
            self.update_object_material()
            self.update_object_modifier()

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


def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)


def unregister():
    bpy.utils.unregister_class(RSN_OT_UpdateParms)
