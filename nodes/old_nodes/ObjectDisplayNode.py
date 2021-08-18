import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RSNodeObjectDisplayNode(RenderNodeBase):
    bl_idname = 'RSNodeObjectDisplayNode'
    bl_label = 'Object Display'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)
    hide_viewport: BoolProperty(name='Hide Viewport', default=False, update=update_node)
    hide_render: BoolProperty(name='Hide Render', default=False, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)

        row = col.row(align=1)
        row.prop(self, "object")

        if self.object:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.object.name

        col.prop(self, 'hide_viewport')
        col.prop(self, 'hide_render')

    def get_data(self):
        task_data_obj = {}
        if self.object:
            task_data_obj[self.name] = {'object'       : f"bpy.data.objects['{self.object.name}']",
                                        'hide_viewport': self.hide_viewport,
                                        'hide_render'  : self.hide_render}

        return task_data_obj


def register():
    bpy.utils.register_class(RSNodeObjectDisplayNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectDisplayNode)
