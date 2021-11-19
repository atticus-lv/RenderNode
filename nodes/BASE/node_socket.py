import bpy
from bpy.props import *
from mathutils import Vector, Euler ,Color

from ._runtime import cache_socket_links, cache_socket_variables


# some method from rigging_node
class SocketBase():

    # reroute method
    ###########################
    @property
    def connected_socket(self):
        '''
        Returns connected socket

        It takes O(len(nodetree.links)) time to iterate thought the links to check the connected socket
        To avoid doing the look up every time, the connections are cached in a dictionary
        The dictionary is emptied whenever a socket/connection/node changes in the nodetree
        accessing links Takes O(len(nodetree.links)) time.
        '''
        self.update_shape()

        _nodetree_socket_connections = cache_socket_links.setdefault(self.id_data, {})
        _connected_socket = _nodetree_socket_connections.get(self, None)

        if _connected_socket:
            return _connected_socket

        socket = self
        if socket.is_output:
            while socket.is_linked and socket.links[0].to_node.bl_rna.name == 'Reroute':
                socket = socket.links[0].to_node.outputs[0]
            if socket.is_linked:
                _connected_socket = socket.links[0].to_socket
        else:
            while socket.is_linked and socket.links[0].from_node.bl_rna.name == 'Reroute':
                socket = socket.links[0].from_node.inputs[0]
            if socket.is_linked:
                _connected_socket = socket.links[0].from_socket

                # set link
                if not socket.is_socket_compatible(_connected_socket):
                    self.set_valid(socket, False)

        cache_socket_links[self.id_data][self] = _connected_socket

        return _connected_socket

    # UI display
    ###################
    @staticmethod
    def set_valid(socket, is_valid=False):
        if socket.links:
            socket.links[0].is_valid = is_valid

    # Link valid
    def is_socket_compatible(self, other_socket):
        if other_socket.bl_idname == 'NodeSocketVirtual':
            return True
        return other_socket.bl_idname == self.bl_idname or other_socket.bl_idname in self.compatible_sockets

    @property
    def ui_value(self):
        '''use for output ui display'''
        val = self.get_value()
        if val is None: return 'None'

        if isinstance(val, bpy.types.Object) or isinstance(val, bpy.types.Material) or isinstance(val, bpy.types.World):
            return val.name
        elif isinstance(val, str) or isinstance(val, int):
            return f'{val}'
        elif isinstance(val, float):
            return f'{round(val, 2)}'
        elif isinstance(val, Vector) or isinstance(val,Color) and  len(val) > 1:
            d_val = [round(num, 2) for num in list(val)]
            return f'{d_val}'
        elif isinstance(val, bool):
            return 'True' if val else 'False'
        else:
            return f'{val.name}' if hasattr(val,'name') else str(val)

    def update_shape(self):
        if hasattr(self, 'shape'):
            if self.display_shape != self.shape: self.display_shape = self.shape

    def remove_incorrect_links(self):
        '''
        Removes the invalid links from the socket when the tree in updated
        There is no visual indication for incorrect custom sockets other than removing the invalid links
        '''
        if self.node.id_data in cache_socket_links:
            del cache_socket_links[self.node.id_data]
        connected_socket = self.connected_socket

        if connected_socket:
            self.unlink()

    def unlink(self):
        '''Unlinks the socket'''
        if self.links:
            print('remove:', self.links[0].from_node, self.links[0].to_node)
            self.id_data.links.remove(self.links[0])

    # set and get method
    #########################
    def set_value(self, value):
        '''Sets the value of an output socket'''
        cache_socket_variables.setdefault(self.id_data, {})[self] = value

    def get_self_value(self):
        '''returns the stored value of an output socket'''
        val = cache_socket_variables.setdefault(self.id_data, {}).get(self, None)
        return val

    def get_value(self):
        '''
        if the socket is an output it returns the stored value of that socket
        if the socket is an input:
            if it's connected, it returns the value of the connected output socket
            if it's not it returns the default value of the socket
        '''
        _value = ''
        if not self.is_output:
            connected_socket = self.connected_socket

            if not connected_socket:
                _value = self.default_value
            else:
                _value = connected_socket.get_self_value()
        else:
            _value = self.get_self_value()

        return _value


def update_node(self, context):
    try:
        self.node.execute_tree()
    except Exception as e:
        # Code marked as unreachable has been executed. Please report this as a bug.
        # Error found at C:\Users\blender\git\blender-vexp\blender.git\source\blender\blenkernel\intern\node.cc:450 in write_node_socket_default_value.
        print('Not able to update in a node group yet')


class RenderNodeSocketmixin():
    '''Used by nodesocket and nodesocketinterface'''

    def init_from_socket(self, node, socket):
        self.display_shape = socket.shape

        if hasattr(self, 'default_value') and hasattr(socket, 'default_value'):
            if hasattr(self, 'set_default_value'):
                self.set_default_value(socket.default_value)
            else:
                self.default_value = socket.default_value


class RenderNodeSocketInterface():
    bl_socket_idname = 'RenderNodeSocket'

    def from_socket(self, node, socket):
        # https://docs.blender.org/api/current/bpy.types.NodeSocketInterface.html#bpy.types.NodeSocketInterface.from_socket
        self.init_from_socket(node, socket)

    def init_socket(self, node, socket, data_path):
        # https://docs.blender.org/api/current/bpy.types.NodeSocketInterface.html#bpy.types.NodeSocketInterface.init_socket
        socket.init_from_socket(node, self)

    def draw_color(self, context):
        '''Color of the socket icon'''
        return self.color

    def draw(self, context, layout):
        if hasattr(self, 'default_value'):
            layout.prop(self, 'default_value', text='Default')


class RenderNodeSocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocket'
    bl_label = 'RenderNodeSocket'

    compatible_sockets = []

    shape = 'CIRCLE'
    color = 0.5, 0.5, 0.5, 1

    show_text:BoolProperty(default=True)
    text: StringProperty(default='')
    default_value: IntProperty(default=0, update=update_node)

    @property
    def display_name(self):
        label = self.name
        if self.text != '':
            label = self.text
        if self.is_output:
            label += ': ' + self.ui_value
        return label

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=self.display_name)
        else:
            layout.prop(self, 'default_value', text=self.display_name if self.show_text else '')


    def draw_color(self, context, node):
        return self.color

    def change_shape(self):
        self.display_shape = self.shape
