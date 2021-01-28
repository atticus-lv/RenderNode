import bpy
from bpy.props import *
from ...node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeObjectDisplayNode(RenderStackNode):
    bl_idname = 'RSNodeObjectDisplayNode'
    bl_label = 'Object Display'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)
    hide_viewport: BoolProperty(name='Hide Viewport', default=False, update=update_node)
    hide_render: BoolProperty(name='Hide Render', default=False, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=0)
        col.prop(self, "object")
        row = col.row(align=1)
        row.prop(self, 'hide_viewport', icon='HIDE_OFF' if not self.hide_viewport else 'HIDE_ON')
        row.prop(self, 'hide_render', icon='RESTRICT_RENDER_OFF' if not self.hide_render else 'RESTRICT_RENDER_ON')


def register():
    bpy.utils.register_class(RSNodeObjectDisplayNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectDisplayNode)
