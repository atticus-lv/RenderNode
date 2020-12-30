import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeFrameRangeInputNode(RenderStackNode):
    bl_idname = "RSNodeFrameRangeInputNode"
    bl_label = "Frame Range"

    frame_start: IntProperty(name="Frame Start", default=1, min=0)
    frame_end: IntProperty(name="Frame End", default=1, min=0)

    use_step: BoolProperty(name="Change Step", default=False)
    frame_step: IntProperty(name="Frame Step", default=1, min=1)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 220

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        row = layout.row(align=1)
        row.prop(self, 'frame_start')
        row.prop(self, 'frame_end')
        row.prop(self, 'use_step', icon_only=1, icon="TRIA_DOWN" if self.use_step else "TRIA_LEFT")
        if self.use_step:
            col = layout.column(align=1)
            col.prop(self, 'frame_step')


def register():
    bpy.utils.register_class(RSNodeFrameRangeInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFrameRangeInputNode)
