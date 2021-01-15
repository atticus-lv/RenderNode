import os
import time
import logging

from bpy.props import *
from RenderStackNode.utility import *

LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


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
    nt = None
    # 渲染状态获取
    _timer = None
    stop = None
    rendering = None
    # mark
    render_mark = None
    mark_task_names = []
    task_data = []
    # item
    frame_list = []
    frame_current = 1

    # 检查当前帧 是否大于任务预设的的帧数
    def frame_check(self):
        if self.frame_current >= self.frame_list[0]["frame_end"]:
            self.mark_task_names.pop(0)
            self.task_data.pop(0)
            self.frame_list.pop(0)
            if len(self.frame_list) > 0:  # 如果帧数列表未空，则继续读取下一个
                self.frame_current = self.frame_list[0]["frame_start"]

        else:
            self.frame_current += self.frame_list[0]["frame_step"]

    # 渲染状态获取
    def pre(self, dummy, thrd=None):
        self.rendering = True

    def update_process_node(self):
        try:
            node = self.nt.nodes['Processor']
            node.done_frames += 1
            node.curr_task = self.mark_task_names[0]
            node.frame_start = bpy.context.scene.frame_start
            node.frame_end = bpy.context.scene.frame_end
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
        pref = bpy.context.preferences.addons.get('RenderStackNode').preferences

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
        pref = bpy.context.preferences.addons.get('RenderStackNode').preferences
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
            self.task_data.append(task_data)
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

    def modal(self, context, event):
        # 计时器内事件
        if event.type == 'TIMER':
            if True in (len(self.mark_task_names) == 0, self.stop is True, len(self.frame_list) == 0):  # 取消或者列表为空 停止
                self.remove_handles()
                bpy.context.window_manager.rsn_running_modal = False
                bpy.context.scene.render.filepath = ""

                self.finish_process_node()

                self.mark_task_names.clear()
                self.frame_list.clear()
                self.task_data.clear()

                return {"FINISHED"}

            elif self.rendering is False:  # 进行渲染
                self.switch2task()
                bpy.context.scene.frame_current = self.frame_current
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

        return {"PASS_THROUGH"}


class RSN_OT_RenderButton(bpy.types.Operator):
    """Need Scene Camera"""
    bl_idname = "rsn.render_button"
    bl_label = "Render"

    render_list_node_name: StringProperty()

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

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.render, 'use_lock_interface', toggle=0)

        box = layout.split().box()
        row = box.row(align = 1)
        row.label(text='Index')
        row.label(text='Task Node')
        row.label(text='Task Label')
        row.label(text='Frame Range')

        col = box.split().box().column(align=1)
        for i, task_node in enumerate(self.mark_task_names):
            row = col.row(align = 1)
            # Index
            row.label(text=f'{i}')
            # node and mute
            node = bpy.context.space_data.edit_tree.nodes[task_node]
            sub = row.row(align=0)
            sub.prop(node, 'mute', text='', icon='PANEL_CLOSE' if node.mute else 'CHECKMARK')
            sub.label(text = task_node)
            # label
            row.label(text=self.task_data[i]['label'])
            # Range
            row.label(text=f'{self.frame_list[i]["frame_start"]}-{self.frame_list[i]["frame_end"]}')

    def execute(self, context):
        blend_path = context.blend_data.filepath

        if blend_path == "":
            self.report({"ERROR"}, "Save your file first!")
            return {"FINISHED"}

        self.change_shading()
        bpy.ops.rsn.render_stack_task(render_list_node_name=self.render_list_node_name)

        return {'FINISHED'}

    def invoke(self, context, event):
        self.nt = None
        self.task_data = []
        self.mark_task_names = []
        self.frame_list = []
        self.get_render_data()
        return context.window_manager.invoke_props_dialog(self,width = 500)


def register():
    bpy.utils.register_class(RSN_OT_RenderStackTask)
    bpy.utils.register_class(RSN_OT_RenderButton)
    bpy.types.WindowManager.rsn_running_modal = BoolProperty(default=False)
    bpy.types.WindowManager.rsn_cur_tree_name = StringProperty(name='current rendering tree', default='')
    bpy.types.WindowManager.rsn_viewer_node = StringProperty(name='Viewer task name')


def unregister():
    bpy.utils.unregister_class(RSN_OT_RenderStackTask)
    bpy.utils.unregister_class(RSN_OT_RenderButton)
    del bpy.types.WindowManager.rsn_running_modal
    del bpy.types.WindowManager.rsn_cur_tree_name
    del bpy.types.WindowManager.rsn_viewer_node
