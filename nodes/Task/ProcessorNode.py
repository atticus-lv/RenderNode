import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


class RSNodeProcessorNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeProcessorNode'
    bl_label = 'Processor'

    active: BoolProperty(default=False)

    task_list: StringProperty()  # store data into node's property
    cur_task: StringProperty()

    # draw properties
    done_col: FloatVectorProperty(name='Done Color', subtype='COLOR', default=(0, 1, 0), min=1, max=1)
    wait_col: FloatVectorProperty(name='Wait Color', subtype='COLOR', default=(0, 0, 0), min=1, max=1)

    def init(self, context):
        self.width = 225

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "done_col")
        layout.prop(self, "wait_col")

    def draw_buttons(self, context, layout):
        if not self.active:
            layout.label(text='Waiting For Render...')
            return None
        task_list = self.task_list.split(',')

        cur_id = task_list.index(self.cur_task)
        total_process = (cur_id + 1) / len(task_list)

        col = layout.column(align=1)
        col.alignment = "CENTER"

        col.label(text=f'Total Process:{round(total_process * 100, 2)} %')
        sub = col.split(factor=total_process, align=1)
        sub.scale_y = 0.25
        sub.prop(self, "done_col", text='')
        sub.prop(self, "wait_col", text='')

        col = layout.column(align=1)
        # process of single task
        for index, task_name in enumerate(task_list):
            # finish list
            if index < cur_id:
                col.box().label(text=task_name, icon="CHECKBOX_HLT")
            # current
            elif index == cur_id:
                if not context.window_manager.rsn_running_modal:
                    box = col.box()
                    box.label(text=task_name, icon="CHECKBOX_HLT")
                    col.label(text='Render Finished!', icon='HEART')
                else:
                    row = col.box().row(align=1)
                    row.label(text=task_name, icon="RENDER_STILL")
                    row.label(text="Process:{:.2f}%".format(
                        context.scene.frame_current / (context.scene.frame_end + 1 - context.scene.frame_start)))
            # waiting
            elif index > cur_id:
                col.box().label(text=task_name, icon="CHECKBOX_DEHLT")


def register():
    bpy.utils.register_class(RSNodeProcessorNode)


def unregister():
    bpy.utils.unregister_class(RSNodeProcessorNode)
