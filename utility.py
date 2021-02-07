import bpy
import json
import logging
from itertools import groupby

from mathutils import Color, Vector


# LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
# logging.basicConfig(format=LOG_FORMAT)
# logger = logging.getLogger('mylogger')


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


class RSN_NodeTree:
    """To store context node tree for getting data in renderstack"""

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


class RSN_Task:
    """Tree method"""

    def __init__(self, node_tree, root_node_name):
        self.nt = node_tree
        self.root_node = self.get_node_from_name(root_node_name)

    def get_node_from_name(self, name):
        try:
            node = self.nt.nodes[name]
            return node
        except KeyError:
            return None

    def get_root_node(self):
        return self.root_node

    def get_sub_node_from_node(self, root_node):
        """Depth first search"""
        node_list = []

        def append_node_to_list(node):
            """Skip the reroute node"""
            if node.bl_idname != 'NodeReroute':
                if len(node_list) == 0 or (len(node_list) != 0 and node.name != node_list[-1]):
                    node_list.append(node.name)

        def get_sub_node(node):
            """Skip the mute node"""
            for input in node.inputs:
                if input.is_linked:
                    sub_node = input.links[0].from_node
                    if sub_node.mute:
                        continue
                    else:
                        get_sub_node(sub_node)
                else:
                    continue
            append_node_to_list(node)

        get_sub_node(root_node)

        return node_list

    def get_sub_node_dict_from_node_list(self, node_list, parent_node_type, black_list=None):
        """Use Task node as separator to get sub nodes in this task"""
        node_list_dict = {}
        if not black_list: black_list = ['RSNodeTaskListNode', 'RSNodeRenderListNode']

        node_list[:] = [node for node in node_list if
                        self.nt.nodes[node].bl_idname not in black_list]
        children_node_list = [list(g) for k, g in
                              groupby(node_list, lambda name: self.nt.nodes[name].bl_idname == parent_node_type) if
                              not k]
        parent_node_list = [node for node in node_list if self.nt.nodes[node].bl_idname == parent_node_type]

        for i in range(len(parent_node_list)):
            try:
                node_list_dict[parent_node_list[i]] = children_node_list[i]
            # release the node behind the parent
            except IndexError:
                pass
        return node_list_dict

    def get_sub_node_from_task(self, task_name, return_dict=False, type='RSNodeTaskNode'):
        """pack method for task node"""
        task = self.get_node_from_name(task_name)
        try:
            node_list = self.get_sub_node_from_node(task)
            if not return_dict:
                return node_list
            else:
                return self.get_sub_node_dict_from_node_list(node_list=node_list,
                                                             parent_node_type=type)
        except AttributeError:
            pass

    def get_sub_node_from_render_list(self, return_dict=False, type='RSNodeTaskNode'):
        """pack method for render list node(get all task)"""
        render_list = self.get_node_from_name(self.root_node.name)
        node_list = self.get_sub_node_from_node(render_list)
        if not return_dict:
            return node_list
        else:
            return self.get_sub_node_dict_from_node_list(node_list=node_list,
                                                         parent_node_type=type)

    def get_task_data(self, task_name, task_dict):
        """transfer nodes to data"""
        task_data = {}
        for node_name in task_dict[task_name]:
            node = self.nt.nodes[node_name]
            task_data['label'] = self.nt.nodes[task_name].label
            if node.bl_idname == "RSNodeCamInputNode":
                task_data["camera"] = node.camera.name if node.camera else None

            elif node.bl_idname == "RSNodeResolutionInputNode":
                task_data["res_x"] = node.res_x
                task_data['res_y'] = node.res_y
                task_data['res_scale'] = node.res_scale

            elif node.bl_idname == "RSNodeCyclesRenderSettingsNode":
                task_data['engine'] = "CYCLES"
                task_data['samples'] = node.samples

            elif node.bl_idname == "RSNodeEeveeRenderSettingsNode":
                task_data['engine'] = "BLENDER_EEVEE"
                task_data['samples'] = node.samples

            elif node.bl_idname == "RSNodeWorkBenchRenderSettingsNode":
                task_data['engine'] = 'BLENDER_WORKBENCH'

            elif node.bl_idname == 'RSNodeLuxcoreRenderSettingsNode':
                task_data['engine'] = 'LUXCORE'
                task_data['luxcore_half'] = {'use_samples': node.use_samples,
                                             'samples'    : node.samples,
                                             'use_time'   : node.use_time,
                                             'time'       : node.time}

            elif node.bl_idname == "RSNodeFrameRangeInputNode":
                if node.frame_end < node.frame_start:
                    node.frame_end = node.frame_start
                task_data["frame_start"] = node.frame_start
                task_data["frame_end"] = node.frame_end
                task_data["frame_step"] = node.frame_step

            elif node.bl_idname == "RSNodeImageFormatInputNode":
                if node.file_format == "JPEG":
                    if node.color_mode == "RGBA":
                        node.color_mode = "RGB"
                    if node.color_depth in ("16", "32"):
                        node.color_depth = "8"

                elif node.file_format == "PNG":
                    if node.color_depth == '32':
                        node.color_depth = "16"

                elif node.file_format == "OPEN_EXR_MULTILAYER":
                    if node.color_depth == "8":
                        node.color_depth = "16"

                task_data['color_mode'] = node.color_mode
                task_data['color_depth'] = node.color_depth
                task_data['file_format'] = node.file_format
                task_data['transparent'] = node.transparent

            elif node.bl_idname == 'RSNodeFilePathInputNode':
                task_data['use_blend_file_path'] = node.use_blend_file_path
                task_data['path_format'] = node.path_format
                task_data['path'] = node.path

            elif node.bl_idname == 'RSNodeScriptsNode':
                if node.type == 'SINGLE':
                    if 'scripts' in task_data:
                        task_data['scripts'][node.name] = node.code
                    else:
                        task_data['scripts'] = {node.name: node.code}
                else:
                    if 'scripts_file' in task_data:
                        task_data['scripts_file'][node.name] = node.file.name
                    else:
                        task_data['scripts_file'] = {node.name: node.file.name}

            elif node.bl_idname == 'RSNodeSmtpEmailNode':
                if 'email' in task_data:
                    task_data['email'][node.name] = {'subject'    : node.subject,
                                                     'content'    : node.content,
                                                     'sender_name': node.sender_name,
                                                     'email'      : node.email}
                else:
                    task_data['email'] = {node.name: {'subject'    : node.subject,
                                                      'content'    : node.content,
                                                      'sender_name': node.sender_name,
                                                      'email'      : node.email}}

            elif node.bl_idname == "RSNodeViewLayerInputNode":
                task_data['view_layer'] = node.view_layer

            elif node.bl_idname == "RSNodeLightStudioNode":
                task_data['ssm_light_studio'] = node.light_studio_index

            elif node.bl_idname == "RSNodeWorldInputNode":
                task_data['world'] = node.world.name

            elif node.bl_idname == "RSNodeActiveRenderSlotNode":
                task_data['render_slot'] = node.active_slot_index

            elif node.bl_idname == 'RSNodeObjectMaterialNode':
                if node.object and node.new_material:
                    if 'object_material' in task_data:
                        task_data['object_material'][node.name] = {'object'      : node.object.name,
                                                                   'slot_index'  : node.slot_index,
                                                                   'new_material': node.new_material.name}
                    else:
                        task_data['object_material'] = {node.name: {'object'      : node.object.name,
                                                                    'slot_index'  : node.slot_index,
                                                                    'new_material': node.new_material.name}}

            elif node.bl_idname == 'RSNodeObjectDataNode':
                value = None
                if node.object:
                    if node.data_path != '':
                        obj, data_path = source_attr(node.object.data, node.data_path)
                        if hasattr(obj, data_path):
                            d_type = type(getattr(obj, data_path, None))
                            if d_type == int:
                                value = node.int_value
                            elif d_type == float:
                                value = node.float_value
                            elif d_type == str:
                                value = node.string_value
                            elif d_type == bool:
                                value = node.bool_value
                            elif d_type == Color:
                                value = list(node.color_value)
                            elif d_type == Vector:
                                value = list(node.vector_value)

                        if value != None:
                            if 'object_data' in task_data:
                                task_data['object_data'][node.name] = {'object'   : node.object.name,
                                                                       'data_path': node.data_path,
                                                                       'value'    : value}
                            else:
                                task_data['object_data'] = {node.name: {'object'   : node.object.name,
                                                                        'data_path': node.data_path,
                                                                        'value'    : value}}


            elif node.bl_idname == 'RSNodeObjectDisplayNode':
                if 'object_display' in task_data:
                    task_data['object_display'][node.name] = {'object'       : node.object.name,
                                                              'hide_viewport': node.hide_viewport,
                                                              'hide_render'  : node.hide_render}
                else:
                    task_data['object_display'] = {node.name: {'object'       : node.object.name,
                                                               'hide_viewport': node.hide_viewport,
                                                               'hide_render'  : node.hide_render}}

            elif node.bl_idname == 'RSNodeObjectPSRNode':
                if node.object and True in {node.use_p, node.use_s, node.use_r}:
                    d = {'object': node.object.name,
                         'use_p' : node.use_p,
                         'use_s' : node.use_s,
                         'use_r' : node.use_r, }

                    if 'object_psr' in task_data:
                        if node.use_p:
                            d['location'] = list(node.p)
                        if node.use_s:
                            d['scale'] = list(node.s)
                        if node.use_r:
                            d['rotation'] = list(node.r)
                        task_data['object_psr'][node.name] = d
                    else:
                        if node.use_p:
                            d['location'] = list(node.p)
                        if node.use_s:
                            d['scale'] = list(node.s)
                        if node.use_r:
                            d['rotation'] = list(node.r)
                        task_data['object_psr'] = {node.name: d}

            elif node.bl_idname == 'RSNodeViewLayerPassesNode':
                if 'view_layer_passes' in task_data:
                    task_data['view_layer_passes'][node.name] = {'view_layer': node.view_layer,
                                                                 'use_passes': node.use_passes}
                else:
                    task_data['view_layer_passes'] = {node.name: {'view_layer': node.view_layer,
                                                                  'use_passes': node.use_passes}}

            elif node.bl_idname == 'RSNodeColorManagementNode':
                task_data['view_transform'] = node.view_transform
                task_data['look'] = node.look
                task_data['ev'] = node.ev
                task_data['gamma'] = node.gamma

            elif node.bl_idname == 'RSNodeTaskInfoInputsNode':
                try:
                    data = json.loads(node.file.as_string())
                    task_data.update(data)
                except Exception:
                    node.use_custom_color = 1
                    node.color = (1, 0, 0)

        return task_data
