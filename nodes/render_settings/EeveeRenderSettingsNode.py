import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def update_node(self, context):
    self.update()


class RSNodeEeveeRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeEeveeRenderSettingsNode'
    bl_label = 'Eevee Settings'

    samples: IntProperty(default=64, min=1, name="Eevee Samples",update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, "samples", text='Samples')

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "samples", text='Samples')
        layout.scale_y = 1.25
        row = layout.row(align=True)
        add = row.operator("rsnode.edit_input", text="Option", icon='ADD')
        add.remove = False
        add.socket_type = "RSNodeSocketRenderSettings"
        add.socket_name = "Option"

        remove = row.operator("rsnode.edit_input", text="Unused", icon='REMOVE')
        remove.remove = True


def register():
    bpy.utils.register_class(RSNodeEeveeRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeEeveeRenderSettingsNode)
