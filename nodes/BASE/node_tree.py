import bpy
import uuid

from bpy.props import *

from ._runtime import cache_node_dependants, cache_socket_links, cache_node_group_outputs, cache_socket_variables
from ._runtime import runtime_info, logger, cache_executed_nodes


# some method comes from rigging_nodes
class NodeTreeBase(bpy.types.NodeTree):
    def get_other_socket(self, socket):
        '''
        Returns connected socket

        It takes O(len(nodetree.links)) time to iterate thought the links to check the connected socket
        To avoid doing the look up every time, the connections are cached in a dictionary
        The dictionary is emptied whenever a socket/connection/node changes in the nodetree
        '''
        # accessing links Takes O(len(nodetree.links)) time.
        _nodetree_socket_connections = cache_socket_links.setdefault(self, {})
        _connected_socket = _nodetree_socket_connections.get(socket, None)

        if _connected_socket:
            return _connected_socket

        socket = socket
        if socket.is_output:
            while socket.links and socket.links[0].to_node.bl_rna.name == 'Reroute':
                socket = socket.links[0].to_node.outputs[0]
            if socket.links:
                _connected_socket = socket.links[0].to_socket
        else:
            while socket.links and socket.links[0].from_node.bl_rna.name == 'Reroute':
                socket = socket.links[0].from_node.inputs[0]
            if socket.links:
                _connected_socket = socket.links[0].from_socket

        cache_socket_links[self][socket] = _connected_socket
        return _connected_socket

    def update(self):
        '''Called when the nodetree sockets or links change, socket pair cache is cleared here'''
        if not runtime_info['executing']:
            if self in cache_socket_links:
                del cache_socket_links[self]
            if self in cache_node_group_outputs:
                del cache_node_group_outputs[self]
            # if self in cache_tree_portals:
            #     del cache_tree_portals[self]
            if self in cache_node_dependants:
                del cache_node_dependants[self]
        else:
            print('TRIED TO UPDATE TREE, BUT ITS EXECUTING')
        # change the socket of the reroute nodes
        for node in self.nodes:
            if node.bl_idname == 'NodeReroute':
                connected = self.get_other_socket(node.inputs[0])
                if connected and connected.bl_idname != node.inputs[
                    0].bl_idname:
                    new_input = node.inputs.new(connected.bl_idname, '')
                    # new_input.init_from_socket(connected.node, connected)
                    new_output = node.outputs.new(connected.bl_idname, '')
                    # new_output.init_from_socket(connected.node, connected)
                    self.relink_socket(node.inputs[0], new_input)
                    self.relink_socket(node.outputs[0], new_output)

                    node.inputs.remove(node.inputs[0])
                    node.outputs.remove(node.outputs[0])

    def relink_socket(self, old_socket, new_socket):
        '''Utility function to relink sockets'''
        if not old_socket.is_output and not new_socket.is_output and old_socket.links:
            self.links.new(old_socket.links[0].from_socket, new_socket)
            self.links.remove(old_socket.links[0])
        elif old_socket.is_output and new_socket.is_output and old_socket.links:
            links = list(old_socket.links[:])
            for link in links:
                self.links.new(new_socket, link.to_socket)
                # self.links.remove(link)

    def execute(self, context):
        task_node = self.nodes.get(bpy.context.window_manager.rsn_viewer_node)
        render_list_node = self.nodes.get(bpy.context.window_manager.rsn_active_list)
        runtime_info['executing'] = True
        cache_socket_variables.clear()

        id = str(uuid.uuid4())
        path = []

        try:
            path.append(bpy.context.space_data.node_tree.name)
            # Execute all the parent trees first up to their active node
            for i in range(0, len(bpy.context.space_data.path) - 1):
                node = bpy.context.space_data.path[i].node_tree.nodes.active_index
                node.execute_dependants(bpy.context, id, path)
                path.append(node.name)

            if task_node: task_node.execute(bpy.context, id, path)
            if render_list_node:
                render_list_node.execute(bpy.context, id, path)

        except Exception as e:
            print(e)

        finally:
            runtime_info['executing'] = False


class RenderStackNodeTree(NodeTreeBase):
    bl_idname = 'RenderStackNodeTree'
    bl_label = 'Render Node Editor'
    bl_icon = 'CAMERA_DATA'


class RenderStackNodeTreeGroup(NodeTreeBase):
    bl_idname = 'RenderStackNodeTreeGroup'
    bl_label = "Render Node (groups)"
    bl_icon = 'NODETREE'

    @classmethod
    def poll(cls, context):
        return False

def clean_draw(self,context):
    pass


def register():
    bpy.types.WindowManager.rsn_active_list = StringProperty(name='Active List',update= clean_draw)

    bpy.utils.register_class(RenderStackNodeTree)
    bpy.utils.register_class(RenderStackNodeTreeGroup)


def unregister():
    bpy.utils.unregister_class(RenderStackNodeTree)
    bpy.utils.unregister_class(RenderStackNodeTreeGroup)

    del bpy.types.WindowManager.rsn_active_list
