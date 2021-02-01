import os
import time
import logging
import json

from bpy.props import *
from ..utility import *
from ..preferences import get_pref
from ..ui.icon_utils import RSN_Preview

LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')

empty_icon = RSN_Preview(image='empty.png', name='empty_icon')


def get_length(frame_list):
    length = 0
    for dict in frame_list:
        length += (dict['frame_end'] + 1 - dict['frame_start']) // dict['frame_step']
    return length


class RSN_OT_RenderStackTask(bpy.types.Operator):
    """Render Tasks"""
    bl_idname = "rsn.render_stack_task"
    bl_label = "Render Stack"

    render_list_node_name: StringProperty()
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='clean path after rendering', default=True)

    nt = None
    # render state
    _timer = None
    stop = None
    rendering = None
    # marker and data list
    render_mark = None
    mark_task_names = []
    task_data_list = []
    frame_list = []
    # frame check
    frame_current = 1

    # 检查当前帧 是否大于任务预设的的帧数
    def frame_check(self):
        if self.frame_current >= self.frame_list[0]["frame_end"]:
            self.mark_task_names.pop(0)
            self.task_data_list.pop(0)
            self.frame_list.pop(0)
            if len(self.frame_list) > 0:  # 如果帧数列表未空，则继续读取下一个
                self.frame_current = self.frame_list[0]["frame_start"]

        else:
            self.frame_current += self.frame_list[0]["frame_step"]

    # set render state
    def pre(self, dummy, thrd=None):
        self.rendering = True

    def update_process_node(self):
        try:
            node = self.nt.nodes['Processor']
            node.done_frames += 1
            node.curr_task = self.mark_task_names[0]
            node.task_data = json.dumps(self.task_data_list[0], indent=2)

            node.frame_start = self.frame_list[0]["frame_start"]
            node.frame_end = self.frame_list[0]["frame_end"]
            node.frame_current = bpy.context.scene.frame_current
        except Exception as e:
            logger.debug(f'Processor {e}')

    def post(self, dummy, thrd=None):
        self.rendering = False
        self.frame_check()
        # show in nodes
        self.update_process_node()

    def cancelled(self, dummy, thrd=None):
        self.stop = True

    # 句柄添加
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

    # 激活下一任务
    def switch2task(self):
        scn = bpy.context.scene
        task = self.mark_task_names[0]
        pref = get_pref()

        bpy.ops.rsn.update_parms(view_mode_handler=task, use_render_mode=True)

        scn.render.use_file_extension = 1
        scn.render.filepath += f"{pref.file_path_separator}{self.frame_current:04d}"

    def init_process_node(self):
        try:
            node = self.nt.nodes['Processor']
            node.count_frames = get_length(self.frame_list)
            node.done_frames = 0
            node.all_tasks = ''
            node.all_tasks = ','.join(self.mark_task_names)
            logger.info(node.all_tasks)
        except Exception as e:
            logger.debug(f'Processor {e}')

    def init_logger(self, node_list_dict):
        pref = get_pref()
        logger.setLevel(int(pref.log_level))
        logger.info(f'Get all data:\n\n{node_list_dict}\n')

    # init 初始化执行
    def execute(self, context):
        context.window_manager.rsn_running_modal = True
        scn = context.scene

        self.stop = False
        self.rendering = False

        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()
        self.nt = rsn_tree.get_wm_node_tree()

        rsn_task = RSN_Task(node_tree=self.nt, root_node_name=self.render_list_node_name)
        node_list_dict = rsn_task.get_sub_node_from_render_list(return_dict=1)

        self.init_logger(node_list_dict)

        for task in node_list_dict:
            task_data = rsn_task.get_task_data(task_name=task, task_dict=node_list_dict)
            self.task_data_list.append(task_data)
            self.mark_task_names.append(task)
            # get frame Range
            render_list = {}
            if "frame_start" in task_data:
                render_list["frame_start"] = task_data["frame_start"]
                render_list["frame_end"] = task_data["frame_end"]
                render_list["frame_step"] = task_data["frame_step"]
            else:
                render_list["frame_start"] = scn.frame_current
                render_list["frame_end"] = scn.frame_current
                render_list["frame_step"] = 1
            self.frame_list.append(render_list)
            # print(self.frame_list)

        if True in (len(self.mark_task_names) == 0, len(self.frame_list) == 0):
            scn.render.use_lock_interface = False
            context.window_manager.rsn_running_modal = False
            self.report({"WARNING"}, 'Nothing to render！')
            return {"FINISHED"}

        self.init_process_node()

        self.frame_current = self.frame_list[0]["frame_start"]
        self.append_handles()

        return {"RUNNING_MODAL"}

    def finish_process_node(self):
        try:
            node = self.nt.nodes['Processor']
            if len(self.mark_task_names) == 0 and len(self.frame_list) == 0:
                node.all_tasks += ',RENDER_FINISHED'
                node.curr_task = 'RENDER_FINISHED'
            else:
                node.all_tasks += ',RENDER_STOPED'
        except Exception as e:
            logger.debug(f'Processor {e}')

    def finish(self):
        self.finish_process_node()
        self.mark_task_names.clear()
        self.frame_list.clear()
        self.task_data_list.clear()
        if self.open_dir:
            try:
                output_dir = os.path.dirname(bpy.context.scene.render.filepath)
                os.startfile(output_dir)
            except:
                logger.warning('RSN File path error, can not open dir after rendering')
        if self.clean_path:
            bpy.context.scene.render.filepath = ""

    def modal(self, context, event):
        # 计时器内事件
        if event.type == 'TIMER':
            if True in (len(self.mark_task_names) == 0, self.stop is True, len(self.frame_list) == 0):  # 取消或者列表为空 停止
                self.remove_handles()
                bpy.context.window_manager.rsn_running_modal = False

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

        rsn_task = RSN_Task(node_tree=self.nt, root_node_name=self.render_list_node_name)
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
        row.prop(context.preferences.view, 'render_display_type')
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
                                      clean_path=self.clean_path)

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

    bpy.types.WindowManager.rsn_running_modal = BoolProperty(default=False)
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
