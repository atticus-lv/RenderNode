import bpy
import json
from itertools import groupby
from collections import deque
from mathutils import Color, Vector
from functools import lru_cache

import numpy as np


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
        try:
            node = self.nt.nodes[name]
            return node
        except KeyError:
            return None

    def get_root_node(self):
        return self.root_node

    def get_children_from_node(self, root_node, pass_mute=True):
        """Depth first search
        :parm root_node: a blender node

        """
        node_list = []

        def append_node_to_list(node):
            """Skip the reroute node"""
            if node.bl_idname != 'NodeReroute':
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
                    # This error shows when the dragging the link off viewer node(Works well with knife tool)
                    # this seems to be a blender error
                    except IndexError:
                        pass
                else:
                    continue
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
                    # This error shows when the dragging the link off viewer node(Works well with knife tool)
                    # this seems to be a blender error
                    except IndexError:
                        pass
                else:
                    continue
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

    def get_children_from_render_list(self, return_dict=False, type='RSNodeTaskNode'):
        """pack method for render list node(get all task)

        """

        render_list = self.get_node_from_name(self.root_node.name)
        node_list = self.get_children_from_node(render_list)
        if not return_dict:
            return node_list
        else:
            return self.get_sub_node_dict_from_node_list(node_list=node_list,
                                                         parent_node_type=type)

    def graph(self):
        node_list = self.get_children_from_node(self.root_node)

    def get_task_data(self, task_name, task_dict):
        """transfer nodes to data
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
            node.debug()
            # task node
            task_node = self.nt.nodes[task_name]
            task_data['name'] = task_name
            task_data['label'] = task_node.label

            # new method
            if node.bl_idname.startswith('RenderNode'):
                node.process()

            # old method/nodes
            #####################

            # Object select Nodes
            elif node.bl_idname == 'RSNodePropertyInputNode':
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
                    if 'scripts' not in task_data:
                        task_data['scripts'] = {}
                    task_data['scripts'].update(node.get_data())
                else:
                    if 'scripts_file' not in task_data:
                        task_data['scripts_file'] = {}
                    task_data['scripts_file'].update(node.get_data())
            # Single node
            else:
                try:
                    task_data.update(node.get_data())
                except TypeError:
                    pass

        return task_data


class RSN_Queue():
    def __init__(self, nodetree, render_list_node: str):
        """init a rsn queue
        :parm nodetree: a blender node tree(rsn node tree)
        :parm render_list_node: name of the render_list_node

        """

        self.nt = nodetree
        self.root_node = render_list_node
        self.task_queue = deque()
        self.task_data_queue = deque()

        self.init_rsn_task()
        self.init_queue()

    def init_rsn_task(self):
        self.rsn = RSN_Nodes(node_tree=self.nt, root_node_name=self.root_node)
        self.task_list_dict = self.rsn.get_children_from_render_list(return_dict=1)

    def init_queue(self):
        """get all the task_data
        fill the key 'frame' for the latter render
        """

        for task in self.task_list_dict:
            task_data = self.rsn.get_task_data(task_name=task, task_dict=self.task_list_dict)

            if "frame_start" not in task_data:
                task_data["frame_start"] = bpy.context.scene.frame_current
                task_data["frame_end"] = bpy.context.scene.frame_current
                task_data["frame_step"] = bpy.context.scene.frame_step

            self.task_queue.append(task)
            self.task_data_queue.append(task_data)

    def is_empty(self):
        return len(self.task_queue) == 0

    def get_length(self):
        return len(self.task_queue)

    def update_task_data(self):
        if not self.is_empty():
            self.task_name = self.task_queue[0]
            self.task_data = self.task_data_queue[0]
            self.frame_start = self.task_data_queue[0]["frame_start"]
            self.frame_end = self.task_data_queue[0]["frame_end"]
            self.frame_step = self.task_data_queue[0]["frame_step"]

    def get_frame_length(self):
        length = 0
        for task_data in self.task_data_queue:
            length += (task_data['frame_end'] + 1 - task_data['frame_start']) // task_data['frame_step']
        return length

    def pop(self):
        if not self.is_empty():
            return self.task_queue.popleft(), self.task_data_queue.popleft()

    def clear_queue(self):
        self.task_queue.clear()
        self.task_data_queue.clear()

        self.task_name = None
        self.task_data = None
        self.frame_start = None
        self.frame_end = None
        self.frame_step = None
