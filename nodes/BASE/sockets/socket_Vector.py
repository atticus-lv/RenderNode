import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase, RenderNodeSocketmixin, RenderNodeSocketInterface
from ..node_socket import update_node


# not register
class RenderNodeSocketInterfaceVector(RenderNodeSocketmixin, RenderNodeSocketInterface, bpy.types.NodeSocketInterface):
    bl_idname = 'RenderNodeSocketVector'
    bl_socket_idname = 'RenderNodeSocketVector'
    bl_label = 'Vector (RenderNode)'

    default_value: FloatVectorProperty(name='Default Value')

    def draw(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'default_value')

    def draw_color(self, context):
        return 0.5, 0.3, 1.0, 1


# not register
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


class RenderNodeSocketInterfaceXYZ(RenderNodeSocketInterfaceVector):
    bl_idname = 'RenderNodeSocketXYZ'
    bl_socket_idname = 'RenderNodeSocketXYZ'
    bl_label = 'Vector (RenderNode)'

    default_value: FloatVectorProperty(name='Default Value', default=(1.0, 1.0, 1.0), subtype='XYZ')


class RenderNodeSocketXYZ(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketXYZ'
    bl_label = 'RenderNodeSocketXYZ'

    default_value: FloatVectorProperty(name='Vector', subtype='XYZ',
                                       update=update_node)


class RenderNodeSocketInterfaceTranslation(RenderNodeSocketInterfaceVector):
    bl_idname = 'RenderNodeSocketTranslation'
    bl_socket_idname = 'RenderNodeSocketTranslation'
    bl_label = 'Translation (RenderNode)'

    default_value: FloatVectorProperty(name='Default Value', subtype='TRANSLATION')


class RenderNodeSocketTranslation(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketTranslation'
    bl_label = 'RenderNodeSocketTranslation'

    default_value: FloatVectorProperty(name='Vector', default=(0, 0, 0), subtype='TRANSLATION',
                                       update=update_node)


class RenderNodeSocketInterfaceEuler(RenderNodeSocketInterfaceVector):
    bl_idname = 'RenderNodeSocketEuler'
    bl_socket_idname = 'RenderNodeSocketEuler'
    bl_label = 'Rotation Euler (RenderNode)'

    default_value: FloatVectorProperty(name='Default Value', subtype='EULER')


class RenderNodeSocketEuler(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketEuler'
    bl_label = 'RenderNodeSocketEuler'

    default_value: FloatVectorProperty(name='Vector', default=(0, 0, 0), subtype='EULER',
                                       update=update_node)


class RenderNodeSocketInterfaceColor(RenderNodeSocketInterfaceVector):
    bl_idname = 'RenderNodeSocketColor'
    bl_socket_idname = 'RenderNodeSocketColor'
    bl_label = 'Color (RenderNode)'

    default_value: FloatVectorProperty(name='Default Value', subtype='COLOR')


class RenderNodeSocketColor(RenderNodeSocketVector, SocketBase):
    bl_idname = 'RenderNodeSocketColor'
    bl_label = 'RenderNodeSocketColor'

    default_value: FloatVectorProperty(update=update_node, subtype='COLOR',
                                       default=(1.0, 1.0, 1.0),
                                       min=0.0, max=1.0)

    def draw_color(self, context, node):
        return 0.9, 0.9, 0.3, 1


classes = (

    RenderNodeSocketVector,
    RenderNodeSocketInterfaceXYZ,
    RenderNodeSocketXYZ,
    RenderNodeSocketInterfaceTranslation,
    RenderNodeSocketTranslation,
    RenderNodeSocketInterfaceEuler,
    RenderNodeSocketEuler,
    RenderNodeSocketInterfaceColor,
    RenderNodeSocketColor,

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
