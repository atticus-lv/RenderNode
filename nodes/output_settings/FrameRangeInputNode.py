import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeFrameRangeInputNode(RenderStackNode):
    bl_idname = "RSNodeFrameRangeInputNode"
    bl_label = "Frame Range"

    frame_start: IntProperty(name="Frame Start", default=1, min=0, update=update_node)
    frame_end: IntProperty(name="Frame End", default=1, min=0, update=update_node)

    use_step: BoolProperty(name="Change Step", default=False, update=update_node)
    frame_step: IntProperty(name="Frame Step", default=1, min=1, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.prop(self, 'frame_start',text='Start')
        row.prop(self, 'frame_end',text='End')
        row.prop(self, 'use_step', icon_only=1, icon="TRIA_DOWN" if self.use_step else "TRIA_LEFT")
        if self.use_step:
            col = layout.column(align=1)
            col.prop(self, 'frame_step')


def register():
    bpy.utils.register_class(RSNodeFrameRangeInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFrameRangeInputNode)
