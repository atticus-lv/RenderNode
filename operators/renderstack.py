import os
import time
import logging
import json

from collections import deque
from bpy.props import *

from ..utility import *
from ..preferences import get_pref
from ..ui.icon_utils import RSN_Preview

LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')

empty_icon = RSN_Preview(image='empty.png', name='empty_icon')


class RSN_Queue():
    def __init__(self, nodetree, render_list_node: str):
        self.nt = nodetree
        self.root_node = render_list_node
        self.task_queue = deque()
        self.task_data_queue = deque()

        self.init_rsn_task()
        self.init_queue()

    def init_rsn_task(self):
        self.rsn = RSN_Nodes(node_tree=self.nt, root_node_name=self.root_node)
        self.task_list_dict = self.rsn.get_sub_node_from_render_list(return_dict=1)

    def init_queue(self):
        for task in self.task_list_dict:
            task_data = self.rsn.get_task_data(task_name=task, task_dict=self.task_list_dict)

            if "frame_start" not in task_data:
                task_data["frame_start"] = bpy.context.scene.frame_current
                task_data["frame_end"] = bpy.context.scene.frame_current
                task_data["frame_step"] = bpy.context.scene.frame_step

            self.task_queue.append(task)
            self.task_data_queue.append(task_data)

    def is_empty(self):
        return len(self.task_queue) == 0

    def get_length(self):
        return len(self.task_queue)

    def update_task_data(self):
        if not self.is_empty():
            self.task_name = self.task_queue[0]
            self.task_data = self.task_data_queue[0]
            self.frame_start = self.task_data_queue[0]["frame_start"]
            self.frame_end = self.task_data_queue[0]["frame_end"]
            self.frame_step = self.task_data_queue[0]["frame_step"]

    def get_frame_length(self):
        length = 0
        for task_data in self.task_data_queue:
            length += (task_data['frame_end'] + 1 - task_data['frame_start']) // task_data['frame_step']
        return length

    def pop(self):
        if not self.is_empty():
            return self.task_queue.popleft(), self.task_data_queue.popleft()

    def clear_queue(self):
        self.task_queue.clear()
        self.task_data_queue.clear()

        self.task_name = None
        self.task_data = None
        self.frame_start = None
        self.frame_end = None
        self.frame_step = None


class RSN_OT_RenderStackTask(bpy.types.Operator):
    """Render Tasks"""
    bl_idname = "rsn.render_stack_task"
    bl_label = "Render Stack"

    render_list_node_name: StringProperty()
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='clean path after rendering', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW')

    ori_render_display_type = None
    nt = None
    # render state
    _timer = None
    stop = None
    rendering = None

    rsn_queue = None
    # frame check
    frame_current = 1

    # set render state
    def pre(self, dummy, thrd=None):
        self.rendering = True

    def post(self, dummy, thrd=None):
        # check and update frame
        self.frame_check()
        # set state (for switch task)
        self.rendering = False
        # show in nodes
        self.update_process_node()

    def cancelled(self, dummy, thrd=None):
        self.stop = True

    # handles
    def append_handles(self):
        bpy.app.handlers.render_pre.append(self.pre)  # 检测渲染状态
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        self._timer = bpy.context.window_manager.event_timer_add(0.2, window=bpy.context.window)  # 添加计时器检测状态
        bpy.context.window_manager.modal_handler_add(self)

    def remove_handles(self):
        bpy.app.handlers.render_pre.remove(self.pre)
        bpy.app.handlers.render_post.remove(self.post)
        bpy.app.handlers.render_cancel.remove(self.cancelled)
        bpy.context.window_manager.event_timer_remove(self._timer)

    # Processor node
    def init_process_node(self):
        try:
            node = self.rsn_queue.nt.nodes['Processor']
            node.count_frames = self.rsn_queue.get_length()
            node.done_frames = 0
            node.all_tasks = ''
            node.all_tasks = ','.join(self.rsn_queue.task_name)
            logger.info(node.all_tasks)
        except Exception as e:
            logger.debug(f'Processor {e}')

    def update_process_node(self):
        try:
            node = self.rsn_queue.nt.nodes['Processor']
            node.done_frames += 1
            node.curr_task = self.rsn_queue.task_name
            node.task_data = json.dumps(self.rsn_queue.task_data, indent=2)

            node.frame_start = self.rsn_queue.frame_start
            node.frame_end = self.rsn_queue.frame_end
            node.frame_current = bpy.context.scene.frame_current
        except Exception as e:
            logger.debug(f'Processor {e}')

    def finish_process_node(self):
        try:
            node = self.rsn_queue.nt.nodes['Processor']
            if self.rsn_queue.is_empty():
                node.all_tasks += ',RENDER_FINISHED'
                node.curr_task = 'RENDER_FINISHED'
            else:
                node.all_tasks += ',RENDER_STOPED'
        except Exception as e:
            logger.debug(f'Processor {e}')

    # init
    def init_logger(self, node_list_dict):
        pref = get_pref()
        logger.setLevel(int(pref.log_level))
        logger.info(f'Get all data:\n\n{node_list_dict}\n')

    def init(self):
        pass

    def execute(self, context):
        context.window_manager.rsn_running_modal = True
        # set state
        self.stop = False
        self.rendering = False
        # set and get tree
        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()

        self.rsn_queue = RSN_Queue(nodetree=rsn_tree.get_wm_node_tree(), render_list_node=self.render_list_node_name)

        if self.rsn_queue.is_empty():
            context.window_manager.rsn_running_modal = False
            self.report({"WARNING"}, 'Nothing to render！')
            return {"FINISHED"}
        # info log
        self.init_logger(self.rsn_queue.task_list_dict)
        self.init_process_node()

        self.rsn_queue.update_task_data()
        self.frame_current = self.rsn_queue.frame_start
        self.append_handles()

        # set render in background
        self.ori_render_display_type = context.preferences.view.render_display_type
        context.preferences.view.render_display_type = self.render_display_type

        return {"RUNNING_MODAL"}

    # update
    def frame_check(self):
        # update task
        self.rsn_queue.update_task_data()

        if self.frame_current >= self.rsn_queue.frame_end:
            self.rsn_queue.pop()
            if not self.rsn_queue.is_empty():  # 如果帧数列表未空，则继续读取下一个
                self.frame_current = self.rsn_queue.frame_start
        else:
            self.frame_current += self.rsn_queue.frame_step

    def switch2task(self):
        scn = bpy.context.scene
        scn.render.use_file_extension = 1

        task = self.rsn_queue.task_name
        bpy.ops.rsn.update_parms(view_mode_handler=task, use_render_mode=True)

        pref = get_pref()
        frame_style = pref.node_file_path.frame_complement
        if frame_style != 'None':
            scn.render.filepath += f"{pref.node_file_path.file_path_separator}{self.frame_current:{frame_style}}"
        else:
            scn.render.filepath += f"{pref.node_file_path.file_path_separator}"

    # finish
    def finish(self):
        # clear_queue/log
        self.finish_process_node()
        self.rsn_queue.clear_queue()
        # open folder
        if self.open_dir:
            try:
                output_dir = os.path.dirname(bpy.context.scene.render.filepath)
                os.startfile(output_dir)
            except:
                logger.warning('RSN File path error, can not open dir after rendering')
        if self.clean_path:
            bpy.context.scene.render.filepath = ""
        # return display type
        bpy.context.preferences.view.render_display_type = self.ori_render_display_type

    def modal(self, context, event):
        if event.type == 'TIMER':
            if True in (self.rsn_queue.is_empty(), self.stop is True):
                # set modal property
                bpy.context.window_manager.rsn_running_modal = False
                self.remove_handles()
                self.finish()

                return {"FINISHED"}

            elif self.rendering is False:  # 进行渲染
                self.switch2task()
                bpy.context.scene.frame_current = self.frame_current
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

        return {"PASS_THROUGH"}


class RSN_OT_ClipBoard(bpy.types.Operator):
    bl_idname = 'rsn.clip_board'
    bl_label = 'Copy'

    data_to_copy: StringProperty(default='Nothing is copied')

    def execute(self, context):
        bpy.context.window_manager.clipboard = self.data_to_copy
        return {'FINISHED'}


class RSN_OT_ShowTaskDetails(bpy.types.Operator):
    bl_idname = 'rsn.show_task_details'
    bl_label = 'Show Details'

    task_data: StringProperty(name='task data (json)')

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
        return context.window_manager.invoke_popup(self, width=300)


class RSN_OT_RenderButton(bpy.types.Operator):
    """Need Scene Camera"""
    bl_idname = "rsn.render_button"
    bl_label = "Render"

    render_list_node_name: StringProperty()
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='Empty filepath after render', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW',
        name='Render Display Type')

    nt = None
    task_data = []
    mark_task_names = []
    frame_list = []

    @classmethod
    def poll(self, context):
        if not context.window_manager.rsn_running_modal:
            return context.scene.camera is not None

    def change_shading(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D' and space.shading.type == "RENDERED":
                        space.shading.type = 'SOLID'

    def get_render_data(self):
        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()
        self.nt = rsn_tree.get_wm_node_tree()

        rsn_task = RSN_Nodes(node_tree=self.nt, root_node_name=self.render_list_node_name)
        node_list_dict = rsn_task.get_sub_node_from_render_list(return_dict=1)

        for task in node_list_dict:
            task_data = rsn_task.get_task_data(task_name=task, task_dict=node_list_dict)
            self.task_data.append(task_data)
            self.mark_task_names.append(task)
            # get frame Range
            render_list = {}
            if "frame_start" in task_data:
                render_list["frame_start"] = task_data["frame_start"]
                render_list["frame_end"] = task_data["frame_end"]
                render_list["frame_step"] = task_data["frame_step"]
            else:
                render_list["frame_start"] = bpy.context.scene.frame_current
                render_list["frame_end"] = bpy.context.scene.frame_current
                render_list["frame_step"] = 1
            self.frame_list.append(render_list)

    def render_options(self, context):
        layout = self.layout.box()
        row = layout.row(align=0)
        sub = row.row(align=1)
        sub.label(text='Open folder after render', icon='FILEBROWSER')
        sub.prop(self, 'open_dir', text='')
        sub = row.row(align=1)
        sub.label(text='Empty filepath after render', icon_value=empty_icon.get_image_icon_id())
        sub.prop(self, 'clean_path', text='')

        row = layout.row(align=0)
        row.prop(self, 'render_display_type')
        row.prop(context.scene.render, 'use_lock_interface', icon_only=1)

    def draw(self, context):
        layout = self.layout

        box = layout.split().box()
        row = box.row(align=1)

        col1 = row.column(align=1).box()
        col2 = row.column(align=1).box()
        col3 = row.column(align=1).box()
        col4 = row.column(align=1).box()
        col5 = row.column(align=1).box()
        col1.scale_x = 0.5
        col5.scale_x = 0.5
        col1.label(text='Index')
        col2.label(text='Task Node')
        col3.label(text='Task Label')
        col4.label(text='Frame Range')
        col5.label(text='Info')

        for i, task_node in enumerate(self.mark_task_names):
            # Index
            col1.label(text=f'{i}')
            # node and mute
            node = bpy.context.space_data.edit_tree.nodes[task_node]
            col2.prop(node, 'mute', text=task_node, icon='PANEL_CLOSE' if node.mute else 'CHECKMARK')
            # label
            col3.label(text=self.task_data[i]['label'])
            # Range
            fs = self.frame_list[i]["frame_start"]
            fe = self.frame_list[i]["frame_end"]
            col4.label(text=f'{fs} → {fe} ({fs - fe + 1})')
            # task_data_list
            d = json.dumps(self.task_data[i], indent=4)
            col5.operator('rsn.show_task_details', icon='INFO', text='').task_data = d

        self.render_options(context)
        layout.separator(factor=0.25)

    def execute(self, context):
        blend_path = context.blend_data.filepath

        if blend_path == "":
            self.report({"ERROR"}, "Save your file first!")
            return {"FINISHED"}
        elif context.scene.render.image_settings.file_format in {'AVI_JPEG', 'AVI_RAW', 'FFMPEG'}:
            self.report({"ERROR"}, "Not Support Anunimation Format")
            return {"FINISHED"}

        self.change_shading()
        bpy.ops.rsn.render_stack_task(render_list_node_name=self.render_list_node_name,
                                      open_dir=self.open_dir,
                                      clean_path=self.clean_path,
                                      render_display_type=self.render_display_type)

        return {'FINISHED'}

    def invoke(self, context, event):
        self.nt = None
        self.task_data = []
        self.mark_task_names = []
        self.frame_list = []
        self.get_render_data()
        return context.window_manager.invoke_props_dialog(self, width=500)


def update_rsn_viewer_node(self, context):
    pass


def register():
    empty_icon.register()

    bpy.utils.register_class(RSN_OT_RenderStackTask)
    bpy.utils.register_class(RSN_OT_ShowTaskDetails)
    bpy.utils.register_class(RSN_OT_ClipBoard)
    bpy.utils.register_class(RSN_OT_RenderButton)

    bpy.types.WindowManager.rsn_running_modal = BoolProperty(default=False, description='poll for the button')
    bpy.types.WindowManager.rsn_cur_tree_name = StringProperty(name='current rendering tree', default='')
    bpy.types.WindowManager.rsn_viewer_node = StringProperty(name='Viewer task name', update=update_rsn_viewer_node)


def unregister():
    empty_icon.unregister()

    bpy.utils.unregister_class(RSN_OT_RenderStackTask)
    bpy.utils.unregister_class(RSN_OT_ClipBoard)
    bpy.utils.unregister_class(RSN_OT_ShowTaskDetails)
    bpy.utils.unregister_class(RSN_OT_RenderButton)

    del bpy.types.WindowManager.rsn_running_modal
    del bpy.types.WindowManager.rsn_cur_tree_name
    del bpy.types.WindowManager.rsn_viewer_node
