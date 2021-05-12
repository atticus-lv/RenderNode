import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


# from ...nodes.BASE.socket_type import RN_SocketObject


def update_node(self, context):
    self.update_parms()


class RenderNodeObjectDisplay(RenderStackNode):
    bl_idname = 'RenderNodeObjectDisplay'
    bl_label = 'Object Display'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)
    hide_viewport: BoolProperty(name='Hide Viewport', default=False, update=update_node)
    hide_render: BoolProperty(name='Hide Render', default=False, update=update_node)

    def init(self, context):
        self.create_prop('RenderNodeSocketObject', 'object', 'Object')
        self.create_prop('RenderNodeSocketBool', 'hide_viewport', 'Hide Viewport')
        self.create_prop('RenderNodeSocketBool', 'hide_render', 'Hide Render')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.width = 200

    def draw_buttons(self, context, layout):
        pass
        # col = layout.column(align=1)
        #
        # row = col.row(align=1)
        # # row.prop(self, "object")
        #
        # row.prop(self, 'hide_viewport', text='',
        #          icon='HIDE_OFF' if not self.hide_viewport else 'HIDE_ON')
        # row.prop(self, 'hide_render', text='',
        #          icon='RESTRICT_RENDER_OFF' if not self.hide_render else 'RESTRICT_RENDER_ON')
        # if self.object:
        #     row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='Select').name = self.object.name

    def get_data(self):
        task_data_obj = {}

        task_data_obj[self.name] = {'object'       : f"bpy.data.objects['{self.inputs['object'].object.name}']",
                                    'hide_viewport': self.inputs['hide_viewport'].bool,
                                    'hide_render'  : self.inputs['hide_render'].bool}
        print(task_data_obj)
        return task_data_obj


def register():
    bpy.utils.register_class(RenderNodeObjectDisplay)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectDisplay)
