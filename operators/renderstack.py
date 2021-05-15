import os
import time
import logging
import json

from bpy.props import *

from ..utility import *
from ..preferences import get_pref
from ..ui.icon_utils import RSN_Preview

# set logger
LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


class RSN_OT_RenderStackTask(bpy.types.Operator):
    """Render all input Tasks"""
    bl_idname = "rsn.render_stack_task"
    bl_label = "Render Queue"

    render_list_node_name: StringProperty()

    # blender properties
    #####################

    render_list_node_name: StringProperty()
    render_list_node = None

    ori_render_display_type = None  # correct display_type after render

    # UI
    processor_node: StringProperty(name='Processor', default='')

    # render state
    ###############
    _timer = None
    stop = None
    rendering = None

    # render queue
    ###############
    queue = None
    frame_start = None
    frame_end = None
    frame_step = None

    # set render state
    def pre(self, dummy, thrd=None):
        self.rendering = True

    def post(self, dummy, thrd=None):
        self.frame_check()
        self.rendering = False

    def cancelled(self, dummy, thrd=None):
        self.stop = True

    # handles
    def append_handles(self):
        bpy.app.handlers.render_pre.append(self.pre)  # 检测渲染状态
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        self._timer = bpy.context.window_manager.event_timer_add(0.1, window=bpy.context.window)  # 添加计时器检测状态
        bpy.context.window_manager.modal_handler_add(self)

    def remove_handles(self):
        bpy.app.handlers.render_pre.remove(self.pre)
        bpy.app.handlers.render_post.remove(self.post)
        bpy.app.handlers.render_cancel.remove(self.cancelled)
        bpy.context.window_manager.event_timer_remove(self._timer)

    def execute(self, context):
        context.window_manager.rsn_running_modal = True
        context.scene.render.use_file_extension = 1
        # set state
        self.stop = False
        self.rendering = False
        # set and get tree
        self.render_list_node = context.space_data.node_tree.nodes.get(self.render_list_node_name)

        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()
        # init RenderQueue
        self.queue = RenderQueue(nodetree=rsn_tree.get_wm_node_tree(),
                                 render_list_node=self.render_list_node)

        if self.queue.is_empty():
            context.window_manager.rsn_running_modal = False
            self.report({"WARNING"}, 'Nothing to render！')
            return {"FINISHED"}

        self.queue.force_update()

        self.append_handles()

        # set render in background
        self.ori_render_display_type = context.preferences.view.render_display_type
        context.preferences.view.render_display_type = self.render_list_node.render_display_type

        return {"RUNNING_MODAL"}
        # return {"FINISHED"}

    # update
    def frame_check(self):
        # update task
        self.queue.force_update()
        self.frame_start, self.frame_end, self.frame_step = self.queue.get_frame_range()

        if not self.queue.is_empty():
            if bpy.context.scene.frame_current >= self.frame_end:
                self.queue.pop()
                self.queue.force_update()
                bpy.context.scene.frame_current = self.frame_start
            else:
                bpy.context.scene.frame_current += self.frame_step
            # show in nodes
            # self.update_process_node()

    def switch2task(self):
        # update task again
        self.queue.force_update()

        bpy.context.scene.render.use_file_extension = 1

    # finish
    def finish(self):
        # clear_queue/log
        # self.finish_process_node()
        self.queue.clear_queue()
        # open folder after render
        if self.render_list_node.open_dir:
            try:
                output_dir = os.path.dirname(bpy.context.scene.render.filepath)
                os.startfile(output_dir)
            except:
                logger.warning('RSN File path error, can not open dir after rendering')
        if self.render_list_node.clean_path:
            bpy.context.scene.render.filepath = ""
        # return display type
        bpy.context.preferences.view.render_display_type = self.ori_render_display_type

    def modal(self, context, event):
        if event.type == 'TIMER':
            if True in (self.queue.is_empty(), self.stop is True):
                # set modal property
                bpy.context.window_manager.rsn_running_modal = False
                self.remove_handles()
                self.finish()

                return {"FINISHED"}

            elif self.rendering is False:
                self.switch2task()
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

        return {"PASS_THROUGH"}


class RSN_OT_ClipBoard(bpy.types.Operator):
    """Copy"""
    bl_idname = 'rsn.clip_board'
    bl_label = 'Copy'

    data_to_copy: StringProperty(default='Nothing is copied')

    def execute(self, context):
        bpy.context.window_manager.clipboard = self.data_to_copy
        return {'FINISHED'}


class RSN_OT_ShowTaskDetails(bpy.types.Operator):
    """Show Details"""
    bl_idname = 'rsn.show_task_details'
    bl_label = 'Show Details'

    task_data: StringProperty(name='task data (json)')
    width: IntProperty(name='Width', default=300)

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        row = layout.split(factor=0.3, align=1)
        row.operator('rsn.clip_board', text='Copy').data_to_copy = self.task_data
        row.label(text='')

        col = layout.box().column(align=1)
        if self.task_data != '':
            l = self.task_data.split('\n')
            for s in l:
                col.label(text=s)

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=self.width)


classes = (
    RSN_OT_RenderStackTask,
    RSN_OT_ShowTaskDetails,
    RSN_OT_ClipBoard,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.rsn_cur_task_list = StringProperty()
    bpy.types.WindowManager.rsn_running_modal = BoolProperty(default=False, description='poll for the button')
    bpy.types.WindowManager.rsn_cur_tree_name = StringProperty(name='current rendering tree', default='')


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.rsn_cur_task_list
    del bpy.types.WindowManager.rsn_running_modal
    del bpy.types.WindowManager.rsn_cur_tree_name
