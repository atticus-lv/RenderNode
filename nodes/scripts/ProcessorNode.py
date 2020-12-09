import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

# import os
# import bpy.utils.previews


class RSNodeProcessorNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeProcessorNode'
    bl_label = 'Processor'

    count_frames: IntProperty(default=1)
    done_frames: IntProperty(default=1)

    all_tasks: StringProperty()
    curr_task: StringProperty()
    frame_start: IntProperty()
    frame_end: IntProperty()
    frame_current: IntProperty()

    green: FloatVectorProperty(subtype='COLOR', default=(0, 1, 0))
    red: FloatVectorProperty(subtype='COLOR', default=(1, 0, 0))

    def init(self, context):
        self.width = 225

    def draw_buttons_ext(self, context, layout):
        layout.prop(self,"green",text="Color 1")
        layout.prop(self,"red",text="Color 2")

    def draw_buttons(self, context, layout):
        done = self.count_frames - self.done_frames
        percent = done / self.count_frames

        col = layout.column(align=1)
        col.scale_y = 1.25
        col.label(text=f"Total: {1 - percent:.0%} | Process: {self.done_frames} / {self.count_frames}")
        row = col.row(align=1)
        sub = row.split(factor=1 - percent, align=1)
        if self.done_frames == 0:
            row.prop(self, 'red', text="")
        else:
            sub.prop(self, 'green', text="")
            sub.prop(self, 'red', text="")

        curr_done = (self.frame_current + 1 - self.frame_start) / (self.frame_end + 1 - self.frame_start)
        task_list = self.all_tasks.split(",")
        layout.separator(factor=0.5)
        if self.all_tasks != '':
            index = task_list.index(self.curr_task)
            for i, name in enumerate(task_list):
                if i < index:
                    box = layout.box().column(align=1)
                    row = box.row()
                    row.label(text=name,icon = 'CHECKBOX_HLT')
                    row = box.row()
                    row.scale_y = 0.5
                    row.prop(self, 'green', text="")

                elif i == index:
                    if name != 'RENDER_FINISHED':
                        box = layout.box().column(align=1)
                        col = box.row().column(align=1)
                        col.label(text=f'{name}',icon = "TRACKING_FORWARDS_SINGLE")

                        row1 = col.row(align=1)
                        row1.label(
                            text=f'Process: {1 - curr_done:.0%} ({self.frame_current + 1 - self.frame_start}/{self.frame_end + 1 - self.frame_start})')
                        row1.label(text=f"| {self.frame_start}>{self.frame_current}<{self.frame_end} |")

                        row = layout.row()
                        row.scale_y = 0.5
                        if 1 - curr_done == 0:
                            row.prop(self, 'red', text="")
                        else:
                            sub = row.split(factor=curr_done, align=1)
                            sub.prop(self, 'green', text="")
                            sub.prop(self, 'red', text="")

                    elif name == 'RENDER_FINISHED':
                        layout.separator(factor=0.5)
                        col = layout.column()
                        col.scale_y = 1.5
                        col.label(text='RENDER FINISHED', icon = 'HEART')

                elif i > index:
                    if not name != 'RENDER_FINISHED':
                        box = layout.box().column(align=1)
                        row = box.row()
                        row.label(text=name,icon = 'CHECKBOX_DEHLT')

                        row = layout.row()
                        row.scale_y = 0.5
                        row.prop(self, 'red', text="")


def register():
    bpy.utils.register_class(RSNodeProcessorNode)


def unregister():
    bpy.utils.unregister_class(RSNodeProcessorNode)
    # bpy.utils.previews.remove("icon_smile")
