import bpy
from ..nodes.BASE._runtime import runtime_info
from mathutils import Vector

import math


class RSN_OP_GroupNodes(bpy.types.Operator):
    bl_idname = "rsn.group_nodes"
    bl_label = "Group nodes"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR" and context.space_data.tree_type == 'RenderStackNodeTree'

    def execute(self, context):
        runtime_info['updating'] = True
        try:
            # Get space, path, current nodetree, selected nodes and a newly created group
            space = context.space_data
            path = space.path
            node_tree = space.path[-1].node_tree
            node_group = bpy.data.node_groups.new("Render Group", "RenderStackNodeTreeGroup")
            selected_nodes = [i for i in node_tree.nodes if i.select]
            nodes_len = len(selected_nodes)

            # Store all links (internal/external) for the selected nodes to be created as group inputs/outputs
            links_external_in = []
            links_external_out = []
            for n in selected_nodes:
                for i in n.inputs:
                    if (i.links):
                        l = i.links[0]
                        if (not l.from_node in selected_nodes):
                            if (not l in links_external_in):
                                links_external_in.append(l)
                for o in n.outputs:
                    if (o.links):
                        for l in o.links:
                            if (not l.to_node in selected_nodes):
                                if (not l in links_external_out):
                                    links_external_out.append(l)

            def sort_in_link(link):
                return link.from_node.location[1]

            def sort_out_link(link):
                return link.to_node.location[1]

            links_external_in.sort(reverse=True, key=sort_in_link)
            links_external_out.sort(reverse=False, key=sort_out_link)

            # Calculate the required locations for placement of grouped node and input/output nodes

            def get_world_location(node):
                location = node.location.copy()
                while node.parent:
                    node = node.parent
                    location += node.location
                return location

            loc_x_in = math.inf
            loc_x_out = -math.inf
            loc_avg = Vector((0, 0))
            for n in selected_nodes:
                loc_avg += get_world_location(n) / nodes_len
                if (get_world_location(n)[0] < loc_x_in):
                    loc_x_in = get_world_location(n)[0]
                if (get_world_location(n)[0] > loc_x_out):
                    loc_x_out = get_world_location(n)[0] + n.width

            # Create and relocate group input & output nodes in the newly created group
            group_input = node_group.nodes.new("NodeGroupInput")
            group_output = node_group.nodes.new("NodeGroupOutput")
            group_input.location = Vector((loc_x_in - 280, loc_avg[1]))
            group_output.location = Vector((loc_x_out + 200, loc_avg[1]))

            # Copy the selected nodes from current nodetree
            # TODO Sometimes crash here
            # it seems to happen when sockets change when in the copy() or update() functions, makes sense
            if (nodes_len > 0):
                bpy.ops.node.clipboard_copy()

            # Create a grouped node with correct location and assign newly created group
            group_node = node_tree.nodes.new("RenderNodeGroup")
            group_node.location = loc_avg
            group_node.node_tree_selection = node_group

            # Add overlay to node editor for the newly created group
            path.append(node_group, node=group_node)

            if (nodes_len > 0):
                # ! if in the copy() node function sockets are changed or deleted this crashes blender, make a check for runtime_info['updating'] before deleting sockets in def copy()
                bpy.ops.node.clipboard_paste()

                for node in node_group.nodes:
                    if not node.parent:
                        node.location = node.location - loc_avg

            for link in links_external_in:
                node = node_group.nodes[link.to_node.name]
                connect_socket = next(x for x in node.inputs if x.identifier == link.to_socket.identifier)
                node_group.links.new(connect_socket, group_input.outputs[-1])
                # correct text
                if hasattr(connect_socket, 'text'): group_input.outputs[-2].text = connect_socket.text

            for link in links_external_out:
                node = node_group.nodes[link.from_node.name]
                connect_socket = next(x for x in node.outputs if x.identifier == link.from_socket.identifier)
                node_group.links.new(connect_socket, group_output.inputs[-1])
                # correct text
                if hasattr(connect_socket, 'text'): group_output.inputs[-2].text = connect_socket.text

            # Add new links to grouped node from original external links
            for i in range(0, len(links_external_in)):
                link = links_external_in[i]

                node = node_tree.nodes[link.from_node.name]
                connect_socket = next(x for x in node.outputs if x.identifier == link.from_socket.identifier)

                node_tree.links.new(connect_socket, group_node.inputs[i])

            for i in range(0, len(links_external_out)):
                link = links_external_out[i]

                node = node_tree.nodes[link.to_node.name]
                connect_socket = next(x for x in node.inputs if x.identifier == link.to_socket.identifier)

                node_tree.links.new(group_node.outputs[i], connect_socket)

            for n in selected_nodes:
                node_tree.nodes.remove(n)

        finally:
            runtime_info['updating'] = False

        return {"FINISHED"}


class RSN_OP_EditGroup(bpy.types.Operator):
    """Edit the group referenced by the active node (or exit the current node-group)"""
    bl_idname = "rsn.edit_group"
    bl_label = "Edit Group"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR" and context.space_data.tree_type == 'RenderStackNodeTree'

    def execute(self, context):
        space = context.space_data
        path = space.path
        node = path[-1].node_tree.nodes.active

        if hasattr(node, "node_tree") and node.select:
            if (node.node_tree):
                path.append(node.node_tree, node=node)
                return {"FINISHED"}
        elif len(path) > 1:
            path.pop()
        return {"CANCELLED"}


def register():
    bpy.utils.register_class(RSN_OP_GroupNodes)
    bpy.utils.register_class(RSN_OP_EditGroup)


def unregister():
    bpy.utils.unregister_class(RSN_OP_GroupNodes)
    bpy.utils.unregister_class(RSN_OP_EditGroup)
