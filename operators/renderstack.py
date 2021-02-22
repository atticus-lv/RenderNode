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

# set custom icon
empty_icon = RSN_Preview(image='empty.png', name='empty_icon')


class RSN_OT_RenderStackTask(bpy.types.Operator):
    """Render Tasks"""
    bl_idname = "rsn.render_stack_task"
    bl_label = "Render Stack"

    # get date from root
    render_list_node_name: StringProperty()

    # action after render
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='clean path after rendering', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW')
    ori_render_display_type = None

    # render state
    _timer = None
    stop = None
    rendering = None
    # get and apply from rsn queue
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
            node.count_frames = self.rsn_queue.get_frame_length()
            node.done_frames = 0
            node.all_tasks = ''
            node.all_tasks = ','.join(self.rsn_queue.task_queue)
        except Exception as e:
            logger.debug(f'Processor {e}')

    def update_process_node(self):
        try:
            node = self.rsn_queue.nt.nodes['Processor']
            node.done_frames += 1
            node.curr_task = self.rsn_queue.task_name
            node.task_data = json.dumps(self.rsn_queue.task_data, indent=2, ensure_ascii=False)

            node.frame_start = self.rsn_queue.frame_start
            node.frame_end = self.rsn_queue.frame_end
            node.frame_current = bpy.context.scene.frame_current
        except:
            pass

    def finish_process_node(self):
        try:
            node = self.rsn_queue.nt.nodes['Processor']
            if self.rsn_queue.is_empty():
                node.all_tasks += ',RENDER_FINISHED'
                node.curr_task = 'RENDER_FINISHED'
            else:
                node.all_tasks += ',RENDER_STOPED'
        except:
            pass

    # init
    def init_logger(self, node_list_dict):
        pref = get_pref()
        logger.setLevel(int(pref.log_level))
        logger.info(f'Get all data:\n{json.dumps(node_list_dict, indent=2, ensure_ascii=False)}\n')

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
        # update for the first render (if there is a viewer node)
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
        # show in nodes
        self.update_process_node()

    def switch2task(self):
        # update task again
        self.rsn_queue.update_task_data()

        scn = bpy.context.scene
        scn.render.use_file_extension = 1
        # update
        task = self.rsn_queue.task_name
        bpy.ops.rsn.update_parms(view_mode_handler=task, use_render_mode=True)
        # set frame complement
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
        # open folder after render
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

            elif self.rendering is False:
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


class RSN_OT_RenderButton(bpy.types.Operator):
    """Need Scene Camera"""
    bl_idname = "rsn.render_button"
    bl_label = "Render"

    # get date from root
    render_list_node_name: StringProperty()

    # action after render
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='Empty filepath after render', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW',
        name='Render Display Type')

    # task_data
    rsn_queue = None

    @classmethod
    def poll(self, context):
        if not context.window_manager.rsn_running_modal:
            return context.scene.camera is not None

    # stop the unnecessary viewport rendering
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

        self.rsn_queue = RSN_Queue(nodetree=rsn_tree.get_wm_node_tree(), render_list_node=self.render_list_node_name)

    def render_options(self, context):
        layout = self.layout.box()
        col = layout.column(align=0)

        sub = col.row(align=1)
        sub.prop(self, 'open_dir', text='')
        sub.label(text='Open folder after render', icon='FILEBROWSER')

        sub = col.row(align=1)
        sub.prop(self, 'clean_path', text='')
        sub.label(text='Empty filepath after render', icon_value=empty_icon.get_image_icon_id())

        split = layout.split(align=0, factor=0.5)
        split.prop(self, 'render_display_type', text='')
        split.separator()
        # split.prop(context.scene.render, 'use_lock_interface', icon_only=1)

    def draw(self, context):
        layout = self.layout

        box = layout.split().box()
        row = box.row(align=1)

        col1 = row.column(align=1).box()
        col2 = row.column(align=1).box()
        col3 = row.column(align=1).box()
        col4 = row.column(align=1).box()
        col5 = row.column(align=1).box()
        col6 = row.column(align=1).box()
        col7 = row.column(align=1).box()

        col1.scale_x = 0.5
        # col2.scale_x = 1.5
        # col5.scale_x = 2.5
        # col6.scale_x = 2
        col7.scale_x = 0.5

        col1.label(text='Index')
        col2.label(text='Node')
        col3.label(text='Label')
        col4.label(text='Frame Range')
        col5.label(text='File Path')
        col6.label(text='File Name')
        col7.label(text='Info')

        for i, task_node in enumerate(self.rsn_queue.task_queue):
            # Index
            col1.label(text=f'{i}')

            # node and mute
            node = bpy.context.space_data.edit_tree.nodes[task_node]
            col2.prop(node, 'mute', text=task_node, icon='PANEL_CLOSE' if node.mute else 'CHECKMARK')

            # label
            col3.label(text=self.rsn_queue.task_data_queue[i]['label'])

            # Range
            fs = self.rsn_queue.task_data_queue[i]["frame_start"]
            fe = self.rsn_queue.task_data_queue[i]["frame_end"]
            col4.label(text=f'{fs} → {fe} ({fe - fs + 1})')

            # filepath
            if 'path' in self.rsn_queue.task_data_queue[i]:
                dir = self.rsn_queue.task_data_queue[i]["path"]
                show = col5.operator('rsn.show_task_details', icon='VIEWZOOM', text='Show')
                show.task_data = dir
                show.width = 500
            else:
                col5.label(text='Not Defined')

            # file name
            if 'path_format' in self.rsn_queue.task_data_queue[i]:
                format = self.rsn_queue.task_data_queue[i]["path_format"]
                show = col6.operator('rsn.show_task_details', icon='VIEWZOOM', text='Show')
                show.task_data = format
                show.width = 500
            else:
                col6.label(text='Not Defined')

            # task_data_list
            d = json.dumps(self.rsn_queue.task_data_queue[i], indent=2, ensure_ascii=False)
            col7.operator('rsn.show_task_details', icon='INFO', text='').task_data = d

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
        self.get_render_data()
        return context.window_manager.invoke_props_dialog(self, width=600)


classes = (
    RSN_OT_RenderStackTask,
    RSN_OT_ShowTaskDetails,
    RSN_OT_ClipBoard,
    RSN_OT_RenderButton
)


def register():
    empty_icon.register()

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.rsn_running_modal = BoolProperty(default=False, description='poll for the button')
    bpy.types.WindowManager.rsn_cur_tree_name = StringProperty(name='current rendering tree', default='')
    bpy.types.WindowManager.rsn_viewer_node = StringProperty(name='Viewer task name')


def unregister():
    empty_icon.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.rsn_running_modal
    del bpy.types.WindowManager.rsn_cur_tree_name
    del bpy.types.WindowManager.rsn_viewer_node
