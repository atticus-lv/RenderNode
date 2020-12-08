import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

class RSNodeLuxcoreRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeLuxcoreRenderSettingsNode'
    bl_label = 'Luxcore Settings'

    use_samples :BoolProperty(name = 'Use Samples',default= True)
    use_time :BoolProperty(name = 'Use Time',default= False)

    time :IntProperty(default = 300 ,min= 1,name = 'Time(s)')
    samples: IntProperty(default=64, min=1, name="Samples")

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")
        self.width = 225

    def draw_buttons(self, context, layout):
        row = layout.row(align = True)
        row.prop(self, "use_samples")
        row.prop(self,"samples")

        row = layout.row(align=True)
        row.prop(self,'use_time')
        row.prop(self,'time')

    def draw_buttons_ext(self, context, layout):
        row = layout.row(align=True)
        row.prop(self, "use_samples")
        row.prop(self, "samples")

        row = layout.row(align=True)
        row.prop(self, 'use_time')
        row.prop(self, 'time')


def register():
    bpy.utils.register_class(RSNodeLuxcoreRenderSettingsNode)

def unregister():
    bpy.utils.unregister_class(RSNodeLuxcoreRenderSettingsNode)