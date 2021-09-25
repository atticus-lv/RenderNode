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


class RSN_OT_SaveQueue(bpy.types.Operator):
    """Save all marked Tasks"""
    bl_idname = "rsn.save_queue"
    bl_label = "Save Task to File"

    # blender properties
    #####################
    render_list_node_name: StringProperty()
    render_list_node = None

    # save queue
    ###############
    queue = None
    origin_path = None

    # poll
    @classmethod
    def poll(self, context):
        return not context.window_manager.rsn_running_modal

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

        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()
        # init RenderQueue
        self.render_list_node = context.space_data.node_tree.nodes.get(self.render_list_node_name)
        self.queue = RenderQueue(nodetree=rsn_tree.get_wm_node_tree(),
                                 render_list_node=self.render_list_node)

        if self.queue.is_empty():
            self.report({"WARNING"}, 'Nothing to Save！')
            return {"FINISHED"}

        self.queue.force_update()
        self.origin_path = bpy.data.filepath

        while not self.queue.is_empty():
            self.queue.force_update()
            task = self.queue.pop()
            path = os.path.join(self.origin_path) + '_' + f'{task}' + '.blend'
            bpy.ops.wm.save_as_mainfile(filepath=path)

        bpy.ops.wm.open_mainfile(filepath=self.origin_path,
                                 display_file_selector=False)

        return {"FINISHED"}


classes = (
    RSN_OT_SaveQueue,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
