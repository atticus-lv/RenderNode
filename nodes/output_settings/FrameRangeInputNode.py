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

    frame_step: IntProperty(name="Frame Step", default=1, min=1, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)

        row = col.row(align=1)
        row.prop(self, 'frame_start', text='Start')
        row.prop(self, 'frame_end', text='End')

        col.prop(self, 'frame_step')

    def get_data(self):
        task_data = {}
        if self.frame_end < self.frame_start:
            self.frame_end = self.frame_start
        task_data["frame_start"] = self.frame_start
        task_data["frame_end"] = self.frame_end
        task_data["frame_step"] = self.frame_step
        return task_data


def register():
    bpy.utils.register_class(RSNodeFrameRangeInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFrameRangeInputNode)
