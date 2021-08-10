import bpy
from bpy.props import *
from mathutils import Vector

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

        cache_socket_links[self.id_data][self] = _connected_socket

        return _connected_socket

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
        elif isinstance(val, tuple) or isinstance(val, Vector):
            d_val = [round(num, 2) for num in list(val)]
            return f'{d_val}'
        elif isinstance(val, bool):
            return 'True' if val else 'False'
        else:
            return f'{val}'

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


def update_node(self, context):
    try:
        self.node.execute_tree()
    except Exception as e:
        print(e)


class RenderNodeSocketInterface(bpy.types.NodeSocketInterface):
    bl_socket_idname = 'RenderNodeSocket'

    def draw(self, context, layout):
        pass

    def draw_color(self, context):
        return (0, 1, 1, 1)


class RenderNodeSocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocket'
    bl_label = 'RenderNodeSocket'

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
            layout.prop(self, 'default_value', text=self.display_name)

    def draw_color(self, context, node):
        return 0.5, 0.5, 0.5, 1


class RenderNodeSocketBool(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketBool'
    bl_label = 'RenderNodeSocketBool'

    default_value: BoolProperty(default=False, update=update_node)

    def draw_color(self, context, node):
        return 0.9, 0.7, 1.0, 1


class RenderNodeSocketInt(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketInt'
    bl_label = 'RenderNodeSocketInt'

    default_value: IntProperty(default=0, update=update_node)

    def draw_color(self, context, node):
        return 0, 0.9, 0.1, 1


class RenderNodeSocketFloat(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketFloat'
    bl_label = 'RenderNodeSocketFloat'

    default_value: FloatProperty(default=0, update=update_node)

    def draw_color(self, context, node):
        return 0.5, 0.5, 0.5, 1


class RenderNodeSocketString(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketString'
    bl_label = 'RenderNodeSocketString'

    default_value: StringProperty(default='', update=update_node)

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1


class RenderNodeSocketFilePath(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketFilePath'
    bl_label = 'RenderNodeSocketFilePath'

    default_value: StringProperty(default='', update=update_node, subtype='FILE_PATH')

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1


# Vector and Subtype
####################

class RenderNodeSocketVector(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketVector'
    bl_label = 'RenderNodeSocketVector'

    default_value: FloatVectorProperty(name='Vector', default=(0, 0, 0), subtype='NONE',
                                       update=update_node)

    def draw(self, context, layout, node, text):
        col = layout.column(align=1)
        if self.is_linked or self.is_output:
            layout.label(text=self.display_name)
        else:
            col.prop(self, 'default_value', text=self.display_name)

    def draw_color(self, context, node):
        return 0.5, 0.3, 1.0, 1


class RenderNodeSocketXYZ(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketXYZ'
    bl_label = 'RenderNodeSocketXYZ'

    default_value: FloatVectorProperty(name='Vector', default=(1.0, 1.0, 1.0), subtype='XYZ',
                                       update=update_node)


class RenderNodeSocketTranslation(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketTranslation'
    bl_label = 'RenderNodeSocketTranslation'

    default_value: FloatVectorProperty(name='Vector', default=(0, 0, 0), subtype='TRANSLATION',
                                       update=update_node)


class RenderNodeSocketEuler(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketEuler'
    bl_label = 'RenderNodeSocketEuler'

    default_value: FloatVectorProperty(name='Vector', default=(0, 0, 0), subtype='EULER',
                                       update=update_node)


class RenderNodeSocketColor(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketColor'
    bl_label = 'RenderNodeSocketColor'

    default_value: FloatVectorProperty(update=update_node, subtype='COLOR',
                                       default=(1.0, 1.0, 1.0),
                                       min=0.0, max=1.0)

    def draw_color(self, context, node):
        return 0.9, 0.9, 0.3, 1


# Object and subtype
##################

class RenderNodeSocketObject(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketObject'
    bl_label = 'RenderNodeSocketObject'

    default_value: PointerProperty(type=bpy.types.Object, update=update_node)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=self.display_name)
        else:
            row = layout.row(align=1)
            row.prop(self, 'default_value', text=self.display_name)
            if self.default_value:
                row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.default_value.name

    def draw_color(self, context, node):
        return 1, 0.6, 0.3, 1


def poll_camera(self, object):
    return object.type == 'CAMERA'


class RenderNodeSocketCamera(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketCamera'
    bl_label = 'RenderNodeSocketCamera'

    default_value: PointerProperty(type=bpy.types.Object, update=update_node, poll=poll_camera)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        if self.is_linked or self.is_output:
            layout.label(text=self.display_name)
        else:
            row.prop(self, 'default_value', text=self.display_name)
            if self.default_value:
                row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.default_value.name

    def draw_color(self, context, node):
        return 1, 0.6, 0.3, 1


# other pointer property
###############

class RenderNodeSocketMaterial(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketMaterial'
    bl_label = 'RenderNodeSocketMaterial'

    default_value: PointerProperty(type=bpy.types.Material, update=update_node)

    def draw_color(self, context, node):
        return 1, 0.4, 0.4, 1


class RenderNodeSocketWorld(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketWorld'
    bl_label = 'RenderNodeSocketWorld'

    default_value: PointerProperty(type=bpy.types.World, update=update_node)

    def draw_color(self, context, node):
        return 1, 0.4, 0.4, 1


class RenderNodeSocketCollection(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketCollection'
    bl_label = 'RenderNodeSocketCollection'

    default_value: PointerProperty(type=bpy.types.Collection, update=update_node)

    def draw_color(self, context, node):
        return 1, 1, 1, 0.5


class RenderNodeSocketViewLayer(RenderNodeSocket, SocketBase):
    bl_idname = 'RenderNodeSocketViewLayer'
    bl_label = 'RenderNodeSocketViewLayer'

    default_value: StringProperty(update=update_node)

    def draw(self, context, layout, node, text):

        row = layout.row(align=1)
        if self.is_linked or self.is_output:
            row.label(text=self.display_name)
        else:
            row.prop_search(self, "default_value", context.scene, "view_layers", text='')

    def draw_color(self, context, node):
        return 0.2, 0.7, 1.0, 1


### old types ###
#################

class RSNodeSocketTaskSettings(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketTaskSettings'
    bl_label = 'RSNodeSocketTaskSettings'

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            io = layout.operator('rsn.search_and_link', text=text, icon='ADD')
            io.node_name = node.name
            if self.is_output:
                io.output_id = int(self.path_from_id()[-2:-1])
                io.input_id = 666
            else:
                io.input_id = int(self.path_from_id()[-2:-1])
                io.output_id = 666
        else:
            layout.label(text=text)

    def draw_color(self, context, node):
        return 0.6, 0.6, 0.6, 1.0


class RSNodeSocketCamera(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketCamera'
    bl_label = 'RSNodeSocketCamera'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0.6, 0.6, 0.6, 1.0


class RSNodeSocketRenderSettings(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketRenderSettings'
    bl_label = 'RSNodeSocketRenderSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0, 1, 0.5, 1.0


class RSNodeSocketOutputSettings(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketOutputSettings'
    bl_label = 'RSNod   eSocketOutputSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 1, 0.8, 0.2, 1.0


class RSNodeSocketRenderList(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'RSNodeSocketRenderList'
    bl_label = 'RSNodeSocketRenderList'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0.95, 0.95, 0.95, 1.0


classes = (
    RSNodeSocketCamera,
    RSNodeSocketRenderSettings,
    RSNodeSocketOutputSettings,
    RSNodeSocketTaskSettings,
    RSNodeSocketRenderList,

    # new
    RenderNodeSocketInterface,
    RenderNodeSocket,
    RenderNodeSocketObject,
    RenderNodeSocketCamera,
    RenderNodeSocketMaterial,
    RenderNodeSocketWorld,
    RenderNodeSocketCollection,
    RenderNodeSocketViewLayer,

    RenderNodeSocketBool,
    RenderNodeSocketInt,
    RenderNodeSocketFloat,
    RenderNodeSocketString,
    RenderNodeSocketFilePath,

    RenderNodeSocketVector,
    RenderNodeSocketXYZ,
    RenderNodeSocketTranslation,
    RenderNodeSocketEuler,
    RenderNodeSocketColor,

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
