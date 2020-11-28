import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def correct_frame(self):
    if self.frame_end < self.frame_start:
        self.frame_end = self.frame_start


class FrameRangeInputNode(RenderStackNode):
    bl_idname = "FrameRangeInputNode"
    bl_label = "Frame Range"

    frame_start: IntProperty(name="Frame Start", default=1, min=0)
    frame_end: IntProperty(name="Frame End", default=1, min=0)
    frame_step: IntProperty(name="Frame Step", default=1, min=1)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'frame_start')
        layout.prop(self, 'frame_end')
        layout.prop(self, 'frame_step')


def register():
    bpy.utils.register_class(FrameRangeInputNode)


def unregister():
    bpy.utils.unregister_class(FrameRangeInputNode)
