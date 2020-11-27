import bpy
from itertools import groupby


class NODE_TREE():
    def __init__(self, node_tree):
        self.nt = node_tree
        self.node_list = self.get_node_list(node_tree.nodes.active)
        self.dict = self.separate_nodes(self.node_list)

    def get_task_info(self, task_name):
        return self.dict[task_name]

    def get_node_list(self, node):
        node_list = []

        def get_node(node):
            if len(node_list) == 0 or (node.name != node_list[-1] and len(node_list) != 0):
                node_list.append(node.name)

        def get_sub_node(node):
            for input in node.inputs:
                if input.is_linked:
                    sub_node = input.links[0].from_node
                    get_sub_node(sub_node)
                else:
                    continue
            # get node itself after get all input nodes
            get_node(node)

        get_sub_node(node)

        return node_list

    def separate_nodes(self, node_list):
        dict = {}
        nt = bpy.context.space_data.edit_tree
        node_list[:] = [node for node in node_list if nt.nodes[node].bl_idname != 'NodeReroute']
        normal_node_list = [list(g) for k, g in
                            groupby(node_list, lambda name: nt.nodes[name].bl_idname == 'RSNodeTaskNode') if not k]
        task_node_list = [node for node in node_list if nt.nodes[node].bl_idname == 'RSNodeTaskNode']

        for i in range(len(task_node_list)):
            dict[task_node_list[i]] = normal_node_list[i]

        return dict
