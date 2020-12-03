import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeCyclesRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCyclesRenderSettingsNode'
    bl_label = 'Cycles Settings'

    samples:IntProperty(default=128,min = 1,name = "Cycles Samples")

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self,"samples",text= 'Samples')

    def draw_buttons_ext(self, context, layout):
        layout.prop(self,"samples",text= 'Samples')
        layout.scale_y = 1.25
        row = layout.row(align=True)
        add = row.operator("rsnode.edit_input", text="Option", icon='ADD')
        add.remove = False
        add.socket_type = "RSNodeSocketRenderSettings"
        add.socket_name = "Option"

        remove = row.operator("rsnode.edit_input", text="Unused", icon='REMOVE')
        remove.remove = True


def register():
    bpy.utils.register_class(RSNodeCyclesRenderSettingsNode)

def unregister():
    bpy.utils.unregister_class(RSNodeCyclesRenderSettingsNode)