import os
import time
import logging
import json

from bpy.props import *

from ..utility import *
from ..preferences import get_pref

# set logger
LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


class RSN_OT_RenderQueue(bpy.types.Operator):
    """Render all marked Tasks"""
    bl_idname = "rsn.render_queue_v2"
    bl_label = "Render All"

    # blender properties
    #####################
    list_node_name: StringProperty()
    render_list_node = None
    ori_render_display_type = None  # correct display_type after render

    # render state
    ###############
    _timer = None
    stop = None
    rendering = None

    # render queue
    ###############
    queue = None

    # poll
    @classmethod
    def poll(self, context):
        if not context.window_manager.rsn_running_modal:
            return context.scene.camera is not None

    # set render state
    def render_init(self, dummy, thrd=None):
        self.rendering = True

    def render_complete(self, dummy, thrd=None):
        self.frame_check()
        self.rendering = False

    def cancelled(self, dummy, thrd=None):
        self.stop = True

    # handles
    def append_handles(self):
        bpy.app.handlers.render_init.append(self.render_init)
        bpy.app.handlers.render_complete.append(self.render_complete)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        self._timer = bpy.context.window_manager.event_timer_add(0.1, window=bpy.context.window)
        bpy.context.window_manager.modal_handler_add(self)

    def remove_handles(self):
        bpy.app.handlers.render_init.remove(self.render_init)
        bpy.app.handlers.render_complete.remove(self.render_complete)
        bpy.app.handlers.render_cancel.remove(self.cancelled)
        bpy.context.window_manager.event_timer_remove(self._timer)

    def stop_viewport_render(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D' and space.shading.type == "RENDERED":
                        space.shading.type = 'SOLID'

    # init
    def execute(self, context):
        # stop viewport rendering
        self.stop_viewport_render()
        context.window_manager.rsn_running_modal = True
        context.scene.render.use_file_extension = 1
        # set state
        self.stop = False
        self.rendering = False
        # set and get tree
        self.render_list_node = context.space_data.node_tree.nodes.get(self.list_node_name)

        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()
        # init RenderQueue
        self.queue = RenderQueueV2(ntree=rsn_tree.get_wm_node_tree(),
                                   render_list_node=self.render_list_node)

        if self.queue.is_empty():
            context.window_manager.rsn_running_modal = False
            self.report({"WARNING"}, 'Nothing to render！')
            return {"FINISHED"}

        # back to the first task
        self.queue.force_update()

        self.append_handles()

        # set render in background
        self.ori_render_display_type = context.preferences.view.render_display_type
        context.preferences.view.render_display_type = self.render_list_node.render_display_type

        return {"RUNNING_MODAL"}

    # update
    def frame_check(self):
        if self.queue.is_empty(): return None

        self.queue.pop()
        self.queue.force_update()

    def switch2task(self):
        # update task again
        self.queue.force_update()

    # finish
    def finish(self):
        self.queue.clear_queue()
        # open folder after render
        if self.render_list_node.open_dir:
            try:
                output_dir = os.path.dirname(bpy.path.abspath(bpy.context.scene.render.filepath))
                os.startfile(output_dir)
            except:
                logger.warning(
                    f'RSN File path error, can not open dir after rendering:\n{bpy.context.scene.render.filepath}')
        if self.render_list_node.clean_path:
            bpy.context.scene.render.filepath = ""
        # return display type
        bpy.context.preferences.view.render_display_type = self.ori_render_display_type

    def modal(self, context, event):
        if event.type == 'ESC':
            # set modal property
            context.window_manager.rsn_running_modal = False
            self.remove_handles()
            self.finish()

        if event.type == 'TIMER':
            if True in (self.queue.is_empty(), self.stop is True):
                # set modal property
                context.window_manager.rsn_running_modal = False
                self.remove_handles()
                self.finish()

                return {"FINISHED"}

            elif self.rendering is False:
                self.switch2task()
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True, animation=True)

        return {"PASS_THROUGH"}


classes = (
    RSN_OT_RenderQueue,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
