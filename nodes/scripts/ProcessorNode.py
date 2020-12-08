import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeProcessorNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeProcessorNode'
    bl_label = 'Processor'

    count_frames: IntProperty(default=1)
    done_frames: IntProperty(default=1)

    c1: FloatVectorProperty(subtype='COLOR', default=(0, 1, 0))
    c2: FloatVectorProperty(subtype='COLOR', default=(1, 0, 0))

    def init(self, context):
        self.width = 175

    def draw_buttons(self, context, layout):
        layout.scale_y = 1.25
        done = self.count_frames - self.done_frames
        percent = done / self.count_frames

        row = layout.box().row(align=1)
        sub = row.split(factor=1 - percent, align=1)

        if self.done_frames == 0:
            row.prop(self, 'c2', text="")
        else:
            sub.prop(self, 'c1', text="")
            sub.prop(self, 'c2', text="")

        layout.label(text=f"{1 - percent:.0%} | Done / All Frames: {self.done_frames} / {self.count_frames}")


def register():
    bpy.utils.register_class(RSNodeProcessorNode)


def unregister():
    bpy.utils.unregister_class(RSNodeProcessorNode)
