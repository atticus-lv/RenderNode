import os
import time

from bpy.props import *
from RenderStackNode.utility import *


def get_length(frame_list):
    length = 0
    for dict in frame_list:
        length += (dict['frame_end'] + 1 - dict['frame_start']) // dict['frame_step']
    return length


class RSN_OT_RenderStackTask(bpy.types.Operator):
    """Render Tasks"""
    bl_idname = "rsn.render_stack_task"
    bl_label = "Render Stack"

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

    def post(self, dummy, thrd=None):
        self.rendering = False
        self.frame_check()
        # show in nodes
        try:
            node = self.nt.nt.nodes['Processor']
            node.done_frames += 1
            node.curr_task = self.mark_task_names[0]
            node.frame_start = bpy.context.scene.frame_start
            node.frame_end = bpy.context.scene.frame_end
            node.frame_current = bpy.context.scene.frame_current
        except:
            pass

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

    def make_path(self, context):
        blend_path = context.blend_data.filepath
        blend_name = bpy.path.basename(blend_path)[:-6]
        task = self.task_data[0]
        if 'path' in task:
            if not task['use_blend_file_path']:
                directory_path = os.path.dirname(task['path']) + "\\" + f"{blend_name}_render"
            else:
                directory_path = os.path.dirname(bpy.data.filepath) + "\\" + f"{blend_name}_render"
            try:
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                return directory_path

            except(Exception) as e:
                self.report({'ERROR'}, f'File Path: Path Error')
                print(directory_path, e)
        else:
            return os.path.dirname(bpy.data.filepath) + "\\"

    def get_postfix(self, scn):
        task = self.task_data[0]
        task_name = task['task_name']
        cam = scn.camera

        postfix = ""
        date_now = str(time.strftime("%m-%d", time.localtime()))
        time_now = str(time.strftime("%H_%M", time.localtime()))

        if 'path_format' in task:
            shot_export_name = task["path_format"]
            for string in shot_export_name.split("/"):
                for r in string.split('$'):
                    if r.startswith("date"):
                        postfix += date_now + '_'
                    elif r.startswith("time"):
                        postfix += time_now + '_'
                    # camera
                    elif r.startswith("camera"):
                        postfix += cam.name + '_'
                    elif r.startswith("res"):
                        postfix += f"{scn.render.resolution_x}x{scn.render.resolution_y}" + "_"
                    elif r.startswith("ev"):
                        postfix += scn.view_settings.exposure + "_"
                    elif r.startswith("view_layer"):
                        postfix += f"{bpy.context.window.view_layer.name}" + '_'
                    elif r.startswith("task"):
                        postfix += task_name + "_"
                    else:
                        postfix += r

                if postfix.endswith("_"): postfix = postfix[:-1]
                postfix += "/"

            if postfix.endswith("/"): postfix = postfix[:-1]

        return postfix

    # 激活下一任务
    def switch2task(self, context):
        scn = context.scene
        task = self.mark_task_names[0]

        bpy.ops.rsn.update_parms(task_name=task)
        # folder path & file name
        directory = self.make_path(context)
        postfix = self.get_postfix(scn)

        frame_format = f"{self.frame_current}"
        if len(f"{self.frame_current}") < 4:
            for i in range(0, 4 - len(f"{self.frame_current}")):
                frame_format = "0" + frame_format

        scn.render.use_file_extension = 1
        scn.render.filepath = os.path.join(directory, postfix + f"_{frame_format}")
        # scn.render.filepath = os.path.join(directory, f"_{frame_format}" + scn.render.file_extension)

    # init 初始化执行
    def execute(self, context):
        context.window_manager.rsn_viewer_modal = False
        context.window_manager.render_stack_modal = True

        scn = context.scene
        scn.render.use_lock_interface = True

        self.stop = False
        self.rendering = False

        nt = NODE_TREE(bpy.context.space_data.edit_tree)
        self.nt = nt
        for task in nt.dict:
            # get data
            task_data = nt.get_task_data(task_name=task)
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

        if True in (len(self.mark_task_names) == 0, len(self.frame_list) == 0):
            scn.render.use_lock_interface = False
            context.window_manager.render_stack_modal = False
            self.report({"WARNING"}, 'Nothing to render！')
            return {"FINISHED"}
        # push to process node
        try:
            node = nt.nt.nodes['Processor']
            node.count_frames = get_length(self.frame_list)
            node.done_frames = 0
            node.all_tasks = ''
            node.all_tasks = ','.join(self.mark_task_names)
            print(node.all_tasks)
        except:
            pass

        self.frame_current = self.frame_list[0]["frame_start"]
        self.append_handles()

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        # 计时器内事件
        if event.type == 'TIMER':
            if True in (len(self.mark_task_names) == 0, self.stop is True, len(self.frame_list) == 0):  # 取消或者列表为空 停止
                self.remove_handles()
                context.window_manager.render_stack_modal = False
                context.scene.render.filepath = ""
                # node
                try:
                    node = self.nt.nt.nodes['Processor']
                    if len(self.mark_task_names) == 0 and len(self.frame_list) == 0:
                        node.all_tasks += ',RENDER_FINISHED'
                        node.curr_task = 'RENDER_FINISHED'
                    else:
                        node.all_tasks += ',RENDER_STOPED'
                except:
                    pass

                self.mark_task_names.clear()
                self.frame_list.clear()
                self.task_data.clear()

                return {"FINISHED"}

            elif self.rendering is False:  # 进行渲染
                self.switch2task(context)
                context.scene.frame_current = self.frame_current
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

        return {"PASS_THROUGH"}


class RSN_OT_RenderButton(bpy.types.Operator):
    bl_idname = "rsn.render_button"
    bl_label = "Render"

    @classmethod
    def poll(self, context):
        if not context.window_manager.render_stack_modal:
            return context.scene.camera is not None

    def change_shading(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D' and space.shading.type == "RENDERED":
                        space.shading.type = 'SOLID'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

    def execute(self, context):
        blend_path = context.blend_data.filepath

        if blend_path == "":
            self.report({"ERROR"}, "Save your file first!")
            return {"FINISHED"}

        self.change_shading()
        bpy.ops.rsn.render_stack_task()

        return {'FINISHED'}

    def invoke(self, context, event):
        self.use_preview_render = False
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(RSN_OT_RenderStackTask)
    bpy.utils.register_class(RSN_OT_RenderButton)
    bpy.types.WindowManager.render_stack_modal = BoolProperty(default=False)


def unregister():
    bpy.utils.unregister_class(RSN_OT_RenderStackTask)
    bpy.utils.unregister_class(RSN_OT_RenderButton)
    del bpy.types.WindowManager.render_stack_modal
