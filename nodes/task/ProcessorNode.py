import bpy
import json
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


# import os
# import bpy.utils.previews


class RSNodeProcessorNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeProcessorNode'
    bl_label = 'Processor'

    count_frames: IntProperty(default=1)
    done_frames: IntProperty(default=1)

    all_tasks: StringProperty()
    curr_task: StringProperty()
    task_data: StringProperty(default='{}')

    frame_start: IntProperty()
    frame_end: IntProperty()
    frame_current: IntProperty()

    green: FloatVectorProperty(subtype='COLOR', default=(0, 1, 0), min=1, max=1)
    red: FloatVectorProperty(subtype='COLOR', default=(0, 0, 0), min=1, max=1)

    def init(self, context):
        self.width = 225

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "green", text="Color 1")
        layout.prop(self, "red", text="Color 2")

    def draw_buttons(self, context, layout):
        done = self.count_frames - self.done_frames
        percent = done / self.count_frames
        # total
        col = layout.column(align=1)
        col.scale_y = 1

        col.label(text=f"Total: {1 - percent:.0%} | Process: {self.done_frames} / {self.count_frames}")

        col1 = col
        row = col.row(align=1)
        sub = row.split(factor=1 - percent, align=1)
        if self.done_frames == 0:
            col1.label(text='Rendering the first image...', icon='SORTTIME')
            row.prop(self, 'red', text="")
        else:
            sub.prop(self, 'green', text="")
            sub.prop(self, 'red', text="")
        # tasks
        curr_done = (self.frame_current - self.frame_start) / (self.frame_end + 1 - self.frame_start)
        task_list = self.all_tasks.split(",")

        layout.separator(factor=0.5)

        if self.all_tasks != '':
            try:
                index = task_list.index(self.curr_task)
                for i, name in enumerate(task_list):
                    # task finish
                    if i < index:
                        box = layout.box().column(align=1)
                        row = box.row()
                        row.label(text=name, icon='CHECKBOX_HLT')
                    # task rendering
                    elif i == index:
                        if name != 'RENDER_FINISHED':

                            box = layout.box().column(align=1)
                            col = box.row().column(align=1)
                            # title
                            label = json.loads(self.task_data)['label']
                            col.label(icon="RECOVER_LAST",
                                      text=f'{name} | {label}')
                            # process bar
                            col.label(
                                text=f"{curr_done:.0%}: {self.frame_start} - {self.frame_current} - {self.frame_end}")
                            col.separator(factor=0.5)
                            row = col.row()
                            row.scale_y = 0.3
                            if 1 - curr_done == 0:
                                row.prop(self, 'red', text="")
                            else:
                                sub = row.split(factor=curr_done, align=1)
                                sub.prop(self, 'green', text="")
                                sub.prop(self, 'red', text="")

                        # last task finish
                        elif name == 'RENDER_FINISHED':
                            layout.separator(factor=0.5)
                            col = layout.column(align=1)
                            col.label(text='RENDER FINISHED', icon='HEART')
                    # task waiting
                    elif i > index and name != 'RENDER_FINISHED':
                        # stop render
                        if name == 'RENDER_STOPED':
                            col = layout.column(align=1)
                            col.label(text='RENDER STOPED', icon='ORPHAN_DATA')
                        # task waiting
                        else:
                            box = layout.box().column(align=1)
                            box.label(text=name, icon='CHECKBOX_DEHLT')
            except:
                pass


def register():
    bpy.utils.register_class(RSNodeProcessorNode)


def unregister():
    bpy.utils.unregister_class(RSNodeProcessorNode)
