import bpy
from bpy.props import *
from ..node_socket import RenderNodeSocket, SocketBase
from ..node_socket import update_node


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


classes = (

    RenderNodeSocketObject,
    RenderNodeSocketCamera,

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
