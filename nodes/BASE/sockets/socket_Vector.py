import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


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


classes = (

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
