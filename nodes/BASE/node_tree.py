import bpy
import nodeitems_utils
from bpy.props import *

from ...utility import *
from ...preferences import get_pref

import logging

LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


class RenderStackNodeTree(bpy.types.NodeTree):
    """RenderStackNodeTree Node Tree"""
    bl_idname = 'RenderStackNodeTree'
    bl_label = 'Render Editor'
    bl_icon = 'CAMERA_DATA'


class RenderStackNode(bpy.types.Node):
    bl_label = "RenderStack Node"

    warning: BoolProperty(name='Is warning', default=False)
    warning_msg: StringProperty(name='warning message', default='')

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'

    ## BASE METHOD
    #########################################

    def copy(self, node):
        self.label = self.name
        print(f"RSN Copied {self.name} from {node.name}")

    def free(self):
        """Remove Node"""
        print("RSN removed node", self.name)

    ## STATE METHOD
    #########################################

    def draw_buttons(self, context, layout):
        if self.warning is True:
            msg = layout.operator('rsn.show_task_details', icon='ERROR', text='Show Waring Message')
            msg.task_data = self.warning_msg

    def debug(self):
        logger.debug(f'pass "{self.name}"')

    def set_warning(self, msg=''):
        self.warning_msg = msg

        self.use_custom_color = 1
        self.color = (1, 0, 0)
        self.warning = True

        logger.warning(f'{self.name}')

    ## UPDATE METHOD
    #########################################

    def update(self):
        """
        The viewer node have this method
        Nodes that need add/remove inputs with have this method
        """
        pass

    def auto_update_inputs(self, socket_type='RSNodeSocketTaskSettings', socket_name='Input'):
        """add or remove inputs automatically
        :parm socket_type: any socket type that is registered in blender
        :parm socket_name: custom name for the socket
        """

        i = 0
        for input in self.inputs:
            if not input.is_linked:
                # keep at least one input for links with py commands
                if i == 0:
                    i += 1
                else:
                    self.inputs.remove(input)
        # auto add inputs
        if i != 1: self.inputs.new(socket_type, socket_name)

    ## RSN DATA MANAGE
    #########################################

    def update_parms(self):
        if bpy.context.window_manager.rsn_node_list != '':
            node_list = bpy.context.window_manager.rsn_node_list.split(',')
            if self.name in node_list:
                pref = get_pref()
                bpy.ops.rsn.update_parms(view_mode_handler=bpy.context.window_manager.rsn_viewer_node,
                                         update_scripts=pref.node_viewer.update_scripts,
                                         use_render_mode=False)

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
