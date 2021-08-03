import os
import logging
import time
import re
import numpy as np

from itertools import groupby
from collections import deque
from functools import lru_cache, wraps

import bpy
from mathutils import Color, Vector

from .preferences import get_pref

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


def source_attr(src_obj, scr_data_path):
    def get_obj_and_attr(obj, data_path):
        path = data_path.split('.')
        if len(path) == 1:
            return obj, path[0]
        else:
            back_obj = getattr(obj, path[0])
            back_path = '.'.join(path[1:])
            return get_obj_and_attr(back_obj, back_path)

    return get_obj_and_attr(src_obj, scr_data_path)


def compare(obj: object, attr: str, val):
    """Use for compare and apply attribute since some properties change may cause depsgraph changes"""
    try:
        if getattr(obj, attr) != val:
            setattr(obj, attr, val)
            logger.debug(f'Attribute "{attr}" SET “{val}”')
    except AttributeError as e:
        logger.info(e)


class RSN_NodeTree:
    """To store context node tree for getting data in RenderQueue"""

    def get_context_tree(self, return_name=False):
        try:
            name = bpy.context.space_data.edit_tree.name
            return bpy.context.space_data.edit_tree.name if return_name else bpy.data.node_groups[name]
        except:
            return None

    def set_wm_node_tree(self, node_tree_name):
        bpy.context.window_manager.rsn_cur_tree_name = node_tree_name

    def get_wm_node_tree(self, get_name=False):
        name = bpy.context.window_manager.rsn_cur_tree_name
        if get_name:
            return name
        else:
            return bpy.data.node_groups[name]

    def set_context_tree_as_wm_tree(self):
        tree_name = self.get_context_tree(return_name=1)
        if tree_name:
            self.set_wm_node_tree(tree_name)


# class RSN_Gpaph:
#     def __init__(self, node_tree, root_node_name):
#         self.nt = node_tree
#         self.root_node = self.get_node_from_name(root_node_name)
#
#     def get_children_from_node(self, root_node, pass_mute=True) -> list:
#         """Depth first search
#         :parm root_node: a blender node
#         nodes append from left to right, from top to bottom
#         """
#         node_list = []
#
#         # @lru_cache(maxsize=None)
#         def get_sub_node(node, pass_mute_node=True):
#             """Recursion
#             :parm node: a blender node
#
#             """
#             for i, input in enumerate(node.inputs):
#                 if input.is_linked:
#                     try:
#                         sub_node = input.links[0].from_node
#                         if sub_node.mute and pass_mute_node: continue
#
#                         get_sub_node(sub_node)
#                     # This error shows when the dragging the link off viewer node(Works well with knife tool)
#                     # this seems to be a blender error
#                     except IndexError:
#                         pass
#                 else:
#                     continue
#             # Skip the reroute node
#             if node.bl_idname != 'NodeReroute':
#                 if len(node_list) == 0 or (len(node_list) != 0 and node.name != node_list[-1]):
#                     node_list.append(node.name)
#
#         get_sub_node(root_node, pass_mute)


class RSN_Nodes:
    """Tree method"""

    def __init__(self, node_tree, root_node_name):
        self.nt = node_tree
        self.root_node = self.get_node_from_name(root_node_name)

    def get_node_from_name(self, name):
        return self.nt.nodes.get(name)

    def get_root_node(self):
        return self.root_node

    def get_children_from_node(self, root_node, pass_mute=True):
        """Depth first search
        :parm root_node: a blender node

        """
        node_list = []

        def append_node_to_list(node):
            """Skip the reroute node"""
            # if node.bl_idname != 'NodeReroute':
            if len(node_list) == 0 or (len(node_list) != 0 and node.name != node_list[-1]):
                node_list.append(node.name)

        # @lru_cache(maxsize=None)
        def get_sub_node(node, pass_mute_node=True):
            """Recursion
            :parm node: a blender node

            """

            for i, input in enumerate(node.inputs):
                if input.is_linked:
                    try:
                        sub_node = input.links[0].from_node
                        if sub_node.mute and pass_mute_node:
                            continue
                        else:
                            get_sub_node(sub_node)
                    except IndexError:  # This error shows when the dragging the link off a node(Works well with knife tool)
                        pass  # this seems to be a blender error
            # nodes append from left to right, from top to bottom
            append_node_to_list(node)

        get_sub_node(root_node, pass_mute)

        return node_list

    def get_sub_node_dict_from_node_list(self, node_list, parent_node_type, black_list=None):
        """Use Task node as separator to get sub nodes in this task
        :parm node_list:
        :parm parent_node_type: node.bl_idname: str
        :parm black_list: list node.bl_idname that you want to skip

        """

        node_list_dict = {}
        if not black_list: black_list = ['RSNodeTaskListNode', 'RSNodeRenderListNode']

        node_list[:] = [node for node in node_list if
                        self.nt.nodes[node].bl_idname not in black_list]
        # separate nodes with the node type input
        children_node_list = [list(g) for k, g in
                              groupby(node_list, lambda name: self.nt.nodes[name].bl_idname == parent_node_type) if
                              not k]
        # get the node type input
        parent_node_list = [node for node in node_list if self.nt.nodes[node].bl_idname == parent_node_type]
        # make a dict {parent name:[children list]}
        for i in range(len(parent_node_list)):
            try:
                node_list_dict[parent_node_list[i]] = children_node_list[i]
            # release the node behind the parent
            except IndexError:
                pass
        return node_list_dict

    def get_children_from_var_node(self, var_node, active, pass_mute=True):
        """Depth first search for the Variants children
        :parm var_node: a blender node
        :parm active:the active input of the Variants node

        """

        black_list = []  # list of nodes to remove from the origin node list

        def append_node_to_list(node):
            """Skip the reroute node"""
            if node.bl_idname != 'NodeReroute':
                if len(black_list) == 0 or (len(black_list) != 0 and node.name != black_list[-1]):
                    if node.bl_idname != 'RSNodeVariantsNode': black_list.append(node.name)

        # @lru_cache(maxsize=None)
        def get_sub_node(node, pass_mute_node=True):
            """Recursion
            :parm node: a blender node

            """

            for i, input in enumerate(node.inputs):
                if input.is_linked and True in (i != active, node.bl_idname != 'RSNodeVariantsNode'):
                    try:
                        sub_node = input.links[0].from_node
                        if sub_node.mute and pass_mute_node:
                            continue
                        else:
                            get_sub_node(sub_node)

                    except IndexError:  # This error shows when the dragging the link off viewer node(Works well with knife tool)
                        pass  # this seems to be a blender error
            # nodes append from left to right, from top to bottom
            append_node_to_list(node)

        get_sub_node(var_node, pass_mute)

        return black_list

    def get_children_from_task(self, task_name, return_dict=False, type='RSNodeTaskNode'):
        """pack method for task node
        :parm task_name: name of the task node
        :parm return_dict: return dict instead of node list
            {'task node name':[
                                children node name1,
                                children node name2]
            }
        :parm type: the bl_idname of the node (key for the dict)

        """

        task = self.get_node_from_name(task_name)
        try:
            node_list = self.get_children_from_node(task)
            # VariantsNodeProperty node in each task
            # only one set VariantsNodeProperty node will be active
            var_collect = {}
            for node_name in node_list:
                set_var_node = self.nt.nodes[node_name]
                if set_var_node.bl_idname == 'RSNodeSetVariantsNode':
                    for item in set_var_node.node_collect:
                        if item.use:
                            var_collect[item.name] = item.active
                    break

            for node_name, active in var_collect.items():
                var_node = self.nt.nodes[node_name]
                black_list = self.get_children_from_var_node(var_node, active)

                node_list = [i for i in node_list if i not in black_list]

            # return clean node list
            if not return_dict:
                return node_list
            else:
                return self.get_sub_node_dict_from_node_list(node_list=node_list,
                                                             parent_node_type=type)
        except AttributeError:
            pass

    def get_task_data(self, task_name, task_dict):
        """transfer nodes to data (OLD METHOD)
        :parm task_name: name of the task node
        :parm task_dict: parse dict
            {'task node name':[
                                children node name1,
                                children node name2]
            }

        """

        task_data = {}

        for node_name in task_dict[task_name]:
            node = self.nt.nodes[node_name]
            if node.bl_idname != 'NodeReroute': node.debug()
            # task node
            task_node = self.nt.nodes[task_name]
            task_data['name'] = task_name
            task_data['label'] = task_node.label

            # old method/nodes
            #####################

            # Object select Nodes
            if node.bl_idname == 'RSNodePropertyInputNode':
                if 'property' not in task_data:
                    task_data['property'] = {}
                task_data['property'].update(node.get_data())

            elif node.bl_idname == 'RSNodeObjectDataNode':
                if 'object_data' not in task_data:
                    task_data['object_data'] = {}
                task_data['object_data'].update(node.get_data())

            elif node.bl_idname == 'RSNodeObjectModifierNode':
                if 'object_modifier' not in task_data:
                    task_data['object_modifier'] = {}
                task_data['object_modifier'].update(node.get_data())

            elif node.bl_idname in 'RSNodeObjectDisplayNode':
                if 'object_display' not in task_data:
                    task_data['object_display'] = {}
                task_data['object_display'].update(node.get_data())

            elif node.bl_idname == 'RSNodeCollectionDisplayNode':
                if 'collection_display' not in task_data:
                    task_data['collection_display'] = {}
                task_data['collection_display'].update(node.get_data())

            elif node.bl_idname == 'RSNodeObjectMaterialNode':
                if 'object_material' not in task_data:
                    task_data['object_material'] = {}
                task_data['object_material'].update(node.get_data())

            elif node.bl_idname == 'RSNodeObjectPSRNode':
                if 'object_psr' not in task_data:
                    task_data['object_psr'] = {}
                task_data['object_psr'].update(node.get_data())

            elif node.bl_idname == 'RSNodeViewLayerPassesNode':
                if 'view_layer_passes' not in task_data:
                    task_data['view_layer_passes'] = {}
                task_data['view_layer_passes'].update(node.get_data())

            elif node.bl_idname == 'RSNodeSmtpEmailNode':
                if 'email' not in task_data:
                    task_data['email'] = {}
                task_data['email'].update(node.get_data())

            elif node.bl_idname == 'RSNodeScriptsNode':
                if node.type == 'SINGLE':
                    if 'ex' not in task_data:
                        task_data['ex'] = {}
                    task_data['ex'].update(node.get_data())
                else:
                    if 'scripts_file' not in task_data:
                        task_data['scripts_file'] = {}
                    task_data['scripts_file'].update(node.get_data())
            # Single node
            else:
                try:
                    task_data.update(node.get_data())
                except (TypeError, AttributeError):  # get from some build-in node like reroute node
                    pass

        return task_data


class RenderQueue():
    def __init__(self, nodetree, render_list_node):
        """init a rsn queue
        :parm nodetree: a blender node tree(rsn node tree)
        :parm render_list_node: render_list_node

        """
        self.nt = nodetree
        self.root_node = render_list_node
        self.task_queue = deque()
        self.frame_range_queue = deque()

        self.task_list = []

        self.init_queue()

    def init_queue(self):
        for item in self.root_node.task_list:
            if item.render:
                self.task_queue.append(item.name)
                self.task_list.append(item.name)
                node = self.nt.nodes[item.name]
                self.frame_range_queue.append([node.frame_start, node.frame_end, node.frame_step])

        # for processing visualization
        bpy.context.window_manager.rsn_cur_task_list = ','.join(self.task_list)
        bpy.context.scene.frame_current = self.frame_range_queue[0][0]

    def is_empty(self):
        return len(self.task_queue) == 0

    def get_frame_range(self):
        self.force_update()
        return self.frame_range_queue[0]

    def force_update(self):
        if not self.is_empty():
            self.nt.nodes[self.task_queue[0]].is_active_task = True

    def pop(self):
        if not self.is_empty():
            self.frame_range_queue.popleft()
            return self.task_queue.popleft()

    def clear_queue(self):
        self.task_queue.clear()
        self.frame_range_queue.clear()

        bpy.context.window_manager.rsn_cur_task_list = ''

# TODO move old update method to old nodes

class RSN_OLD_TaskUpdater():
    def __init__(self, node_tree, task_data):
        self.task_data = task_data
        self.nt = node_tree

    def warning_node_color(self, node_name, msg=''):
        """
        :parm e: error message
        use try to catch error because user may use task info node to input settings

        """
        try:
            node = self.nt.nodes[node_name]
            node.set_warning(msg=msg)
        except Exception as e:
            print(e)

    def update_all(self):
        if not self.task_data: return None

        pref = get_pref()

        self.update_camera()
        self.update_color_management()
        self.update_res()
        self.update_render_engine()

        self.update_property()

        self.update_collection_display()

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

        if pref.node_task.update_scripts:
            self.updata_scripts()
        if pref.node_task.update_path:
            self.update_path()
        if pref.node_task.update_view_layer_passes:
            self.update_view_layer_passes()

        self.send_email()

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
            if task['path'] == '//':
                directory_path = bpy.path.abspath(task['path'])
            else:
                directory_path = os.path.dirname(task['path'])
            try:
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                return directory_path
            except Exception as e:
                self.report({'ERROR'}, f'File Path: No Such a Path')
        else:
            return '//'

    def get_postfix(self):
        """path expression"""
        scn = bpy.context.scene
        cam = scn.camera

        blend_name = ''
        postfix = ''

        if 'path' in self.task_data:

            postfix = self.task_data["path_expression"]
            # replace camera name
            if cam:
                postfix = postfix.replace('$camera', cam.name)
            else:
                postfix = postfix
            # replace engine
            postfix = postfix.replace('$engine', bpy.context.scene.render.engine)
            # replace res
            postfix = postfix.replace('$res', f"{scn.render.resolution_x}x{scn.render.resolution_y}")
            # replace label
            postfix = postfix.replace('$label', self.task_data["label"])
            # replace view_layer
            postfix = postfix.replace('$vl', bpy.context.view_layer.name)
            # version_
            postfix = postfix.replace('$V', self.task_data["version"])

            # frame completion
            STYLE = re.findall(r'([$]F\d)', postfix)
            if len(STYLE) > 0:
                c_frame = bpy.context.scene.frame_current
                for i, string in enumerate(STYLE):
                    format = f'0{STYLE[i][-1:]}d'
                    postfix = postfix.replace(STYLE[i], f'{c_frame:{format}}')

            # time format
            TIME = re.findall(r'([$]T{.*?})', postfix)
            if len(TIME) > 0:
                for i, string in enumerate(TIME):
                    format = time.strftime(TIME[i][3:-1], time.localtime())
                    postfix = postfix.replace(TIME[i], format)

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

    def update_property(self):
        if 'property' in self.task_data:
            for node_name, dict in self.task_data['property'].items():
                try:
                    obj = eval(dict['full_data_path'])
                    value = dict['value']
                    if obj != value:
                        exec(f"{dict['full_data_path']}={value}")
                except Exception as e:
                    self.warning_node_color(node_name, f'Full data path error!\n{e}')

    def update_object_display(self):
        if 'object_display' in self.task_data:
            for node_name, dict in self.task_data['object_display'].items():
                ob = eval(dict['object'])
                compare(ob, 'hide_viewport', dict['hide_viewport'])
                compare(ob, 'hide_render', dict['hide_render'])

    def update_collection_display(self):
        if 'collection_display' in self.task_data:
            for node_name, dict in self.task_data['collection_display'].items():
                ob = eval(dict['collection'])
                compare(ob, 'hide_viewport', dict['hide_viewport'])
                compare(ob, 'hide_render', dict['hide_render'])

    def update_object_psr(self):
        if 'object_psr' in self.task_data:
            for node_name, dict in self.task_data['object_psr'].items():
                ob = eval(dict['object'])
                if 'location' in dict:
                    compare(ob, 'location', dict['location'])
                if 'scale' in dict:
                    compare(ob, 'scale', dict['scale'])
                if 'rotation' in dict:
                    compare(ob, 'rotation_euler', dict['rotation'])

    def update_object_material(self):
        if 'object_material' in self.task_data:
            for node_name, dict in self.task_data['object_material'].items():
                ob = eval(dict['object'])
                try:
                    if ob.material_slots[dict['slot_index']].material.name != dict['new_material']:
                        ob.material_slots[dict['slot_index']].material = bpy.data.materials[dict['new_material']]
                except Exception as e:
                    pass

    def update_object_data(self):
        if 'object_data' in self.task_data:
            for node_name, dict in self.task_data['object_data'].items():
                ob = eval(dict['object'])
                value = dict['value']
                obj, attr = source_attr(ob.data, dict['data_path'])
                compare(obj, attr, value)

    def update_object_modifier(self):
        if 'object_modifier' in self.task_data:
            for node_name, dict in self.task_data['object_modifier'].items():
                ob = eval(dict['object'])
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
                    self.warning_node_color(node_name, str(e))

    def updata_view_layer(self):
        if 'view_layer' in self.task_data and bpy.context.window.view_layer.name != self.task_data['view_layer']:
            bpy.context.window.view_layer = bpy.context.scene.view_layers[self.task_data['view_layer']]

    def updata_scripts(self):
        if 'ex' in self.task_data:
            for node_name, value in self.task_data['ex'].items():
                try:
                    exec(value)
                except Exception as e:
                    self.warning_node_color(node_name, str(e))

        if 'scripts_file' in self.task_data:
            for node_name, file_name in self.task_data['scripts_file'].items():
                try:
                    c = bpy.data.texts[file_name].as_string()
                    exec(c)
                except Exception as e:
                    self.warning_node_color(node_name, str(e))

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
        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH'] + [engine.bl_idname for engine in
                                                            bpy.types.RenderEngine.__subclasses__()]

        has_engine = None
        # engine settings
        if 'engine' in self.task_data:
            if self.task_data['engine'] in engines:
                compare(bpy.context.scene.render, 'engine', self.task_data['engine'])
                has_engine = True
        # samples
        if 'samples' in self.task_data:
            if self.task_data['engine'] == "BLENDER_EEVEE":
                compare(bpy.context.scene.eevee, 'taa_render_samples', self.task_data['samples'])
            elif self.task_data['engine'] == "CYCLES":
                compare(bpy.context.scene.cycles, 'samples', self.task_data['samples'])

        # CYCLES
        if 'cycles_light_path' in self.task_data:
            for key, value in self.task_data['cycles_light_path'].items():
                compare(bpy.context.scene.cycles, key, value)

        if not has_engine: return None
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

    def update_res(self):
        if 'res_x' in self.task_data:
            rn = bpy.context.scene.render
            compare(rn, 'resolution_x', self.task_data['res_x'])
            compare(rn, 'resolution_y', self.task_data['res_y'])
            compare(rn, 'resolution_percentage', self.task_data['res_scale'])

    def update_camera(self):
        if 'camera' in self.task_data and self.task_data['camera']:
            cam = eval(self.task_data['camera'])
            if cam: compare(bpy.context.scene, 'camera', cam)
