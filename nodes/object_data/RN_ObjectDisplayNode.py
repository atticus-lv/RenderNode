import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
# from ...nodes.BASE.socket_type import RN_SocketObject


def update_node(self, context):
    self.update_parms()


class RN_ObjectDisplayNode(RenderStackNode):
    bl_idname = 'RN_ObjectDisplayNode'
    bl_label = 'Object Display'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)
    hide_viewport: BoolProperty(name='Hide Viewport', default=False, update=update_node)
    hide_render: BoolProperty(name='Hide Render', default=False, update=update_node)

    socket_value_update = update_node

    def init(self, context):
        self.inputs.new('RN_SocketObject', "Object")
        # self.inputs.new('NodeSocketBool', "Hide Viewport")
        # self.inputs.new('NodeSocketBool', "Hide Render")
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)

        row = col.row(align=1)
        # row.prop(self, "object")

        row.prop(self, 'hide_viewport', text='',
                 icon='HIDE_OFF' if not self.hide_viewport else 'HIDE_ON')
        row.prop(self, 'hide_render', text='',
                 icon='RESTRICT_RENDER_OFF' if not self.hide_render else 'RESTRICT_RENDER_ON')
        if self.object:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='Select').name = self.object.name

    def update(self):
        # if self.inputs['Object'].is_linked:

        if self.inputs['Object'].is_linked is False and self.inputs['Object']:
            self.object = self.inputs['Object'].object
        elif self.inputs['Object'].is_linked is False and not self.inputs['Object']:
            self.object = None


    def get_data(self):
        task_data_obj = {}
        if self.object:
            task_data_obj[self.name] = {'object'       : f"bpy.data.objects['{self.object.name}']",
                                        'hide_viewport': self.hide_viewport,
                                        'hide_render'  : self.hide_render}

        return task_data_obj


def register():
    bpy.utils.register_class(RN_ObjectDisplayNode)


def unregister():
    bpy.utils.unregister_class(RN_ObjectDisplayNode)
