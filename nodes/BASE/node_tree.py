import bpy
import nodeitems_utils
from bpy.props import *

from ...utility import *
from ...preferences import get_pref

import logging
from functools import wraps

LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


def get_data_log(fn):
    @wraps(fn)
    def print_arg(*args, **kwargs):
        logger.debug(f'pass "{args[0].name}"')
        result = fn(*args, **kwargs)
        return result

    return print_arg


class RenderStackNodeTree(bpy.types.NodeTree):
    """RenderStackNodeTree Node Tree"""
    bl_idname = 'RenderStackNodeTree'
    bl_label = 'Render Editor'
    bl_icon = 'CAMERA_DATA'


class RenderStackNode(bpy.types.Node):
    bl_label = "RenderStack Node"

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'

    def copy(self, node):
        print("RSN Copied node", node.name)

    def free(self):
        """Remove Node"""
        print("RSN removed node", self.name)

    def update(self):
        """
        The viewer node have this method
        Nodes that need add/remove inputs with have this method
        """
        pass

    # RSN method
    def auto_update_inputs(self):
        """add or remove inputs"""
        if self.bl_idname == 'RSNodeTaskNode':
            pass
        elif self.bl_idname == 'RSNodeRenderListNode':
            pass

    def update_parms(self):
        if bpy.context.window_manager.rsn_node_list != '':
            node_list = bpy.context.window_manager.rsn_node_list.split(',')
            if self.name in node_list:
                pref = get_pref()
                bpy.ops.rsn.update_parms(view_mode_handler=bpy.context.window_manager.rsn_viewer_node,
                                         update_scripts=pref.node_viewer.update_scripts,
                                         use_render_mode=False)

    @get_data_log
    def debug(self):
        """Debug Log"""
        pass

    def set_warning(self):
        self.use_custom_color = 1
        self.color = (1, 0, 0)
        logger.warning(f'{self.name}')

    def get_data(self):
        """For get self date into rsn tree method"""
        pass

    def apply_data(self, task_data):
        """apply self data with update parm ops"""
        pass


class RenderStackNodeGroup(bpy.types.NodeCustomGroup):
    bl_label = 'RenderStack Node Group'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'


classes = (
    RenderStackNodeTree,
    RenderStackNode,
    RenderStackNodeGroup,

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
