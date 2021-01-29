import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeLuxcoreRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeLuxcoreRenderSettingsNode'
    bl_label = 'Luxcore Settings'

    use_samples: BoolProperty(name='Use Samples', default=True,update=update_node)
    use_time: BoolProperty(name='Use Time', default=False,update=update_node)

    time: IntProperty(default=300, min=1, name='Time(s)',update=update_node)
    samples: IntProperty(default=64, min=1, name="Samples",update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")
        self.width = 225

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        row = col.row(align=True)
        row.prop(self, "use_samples")
        row.prop(self, "samples")

        row = col.row(align=True)
        row.prop(self, 'use_time')
        row.prop(self, 'time')

    def draw_buttons_ext(self, context, layout):
        col = layout.column(align=1)
        row = col.row(align=True)
        row.prop(self, "use_samples")
        row.prop(self, "samples")

        row = col.row(align=True)
        row.prop(self, 'use_time')
        row.prop(self, 'time')


def register():
    bpy.utils.register_class(RSNodeLuxcoreRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeLuxcoreRenderSettingsNode)
