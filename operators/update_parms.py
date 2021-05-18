import bpy
from bpy.props import StringProperty, BoolProperty
from ..utility import *
from ..preferences import get_pref

import time
import os
import re


class RSN_OT_UpdateParms(bpy.types.Operator):
    """Update RSN parameters"""
    bl_idname = "rsn.update_parms"
    bl_label = "Update Parms"

    use_render_mode: BoolProperty(default=True, description="Prevent from python context error")

    view_mode_handler: StringProperty()
    update_scripts: BoolProperty(default=False)

    nt: None
    task_data = None

    def execute(self, context):
        """update_parm method"""
        self.data_changes()
        return {'FINISHED'}

    def reroute(self, node):
        """help to ignore the reroute node"""

        def is_task_node(node):
            """return the task_node only"""
            if node.bl_idname == "RSNodeTaskNode":
                return node.name

            sub_node = node.inputs[0].links[0].from_node

            return is_task_node(sub_node)

        task_node_name = is_task_node(node)
        return task_node_name

    def warning_node_color(self, node_name, msg=''):
        """
        :parm e: error message
        use try to catch error because user may use task info node to input settings

        """
        try:
            node = self.nt.nodes[node_name]
            node.set_warning(msg=msg)
        except Exception as e:
            print(e)

    # first get task data
    def get_data(self):
        """Viewer mode and render mode.Prevent the python state error"""

        if not self.use_render_mode:
            # read the node tree from context space_data
            rsn_tree = RSN_NodeTree()
            self.nt = rsn_tree.get_context_tree()
        else:
            # read the node tree from window_manager
            rsn_tree = RSN_NodeTree()
            self.nt = rsn_tree.get_wm_node_tree()

        rsn_task = RSN_Nodes(node_tree=self.nt,
                             root_node_name=self.view_mode_handler)
        # get the task node and the sub node, return dict
        node_list_dict = rsn_task.get_children_from_task(task_name=self.view_mode_handler,
                                                         return_dict=True)
        # if the task have sub node, get the data of them
        if node_list_dict:
            self.task_data = rsn_task.get_task_data(task_name=self.view_mode_handler,
                                                    task_dict=node_list_dict)
        if self.task_data:
            logger.debug(f'Get Task "{self.view_mode_handler}"')
        else:
            logger.debug(f'Not task is linked to the viewer')

        return node_list_dict

    def data_changes(self):
        pref = get_pref()
        logger.setLevel(int(pref.log_level))

        node_list_dict = self.get_data()

        old_method = RSN_OLD_TaskUpdater(self.nt, self.task_data)
        old_method.update_all()

        # new method
        if node_list_dict:
            # new method
            for task_name, node_list in node_list_dict.items():
                for node_name in node_list:
                    node = self.nt.nodes[node_name]
                    if node.bl_idname.startswith('RenderNode'): node.process()


def register():
    bpy.utils.register_class(RSN_OT_UpdateParms)


def unregister():
    bpy.utils.unregister_class(RSN_OT_UpdateParms)
