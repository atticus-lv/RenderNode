import bpy
import nodeitems_utils
from bpy.props import *

from ...utility import *
from ...preferences import get_pref


class RenderStackNodeTree(bpy.types.NodeTree):
    """RenderStackNodeTree Node Tree"""
    bl_idname = 'RenderStackNodeTree'
    bl_label = 'Render Editor'
    bl_icon = 'CAMERA_DATA'


def node_warning(self, context):
    if self.warning:
        try:
            self.use_custom_color = 1
            self.color = (1, 0, 0)
        except:
            pass


class RenderStackNode(bpy.types.Node):
    bl_label = "RenderStack Node"

    warning: BoolProperty(default=False, update=node_warning)

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'

    def copy(self, node):
        print("RSN Copied node", node.name)

    def free(self):
        print("RSN removed node", self.name)

    def update(self):
        pass

    def update_parms(self):
        if bpy.context.window_manager.rsn_node_list != '':
            node_list = bpy.context.window_manager.rsn_node_list.split(',')
            if self.name in node_list:
                pref = get_pref()
                bpy.ops.rsn.update_parms(view_mode_handler=bpy.context.window_manager.rsn_viewer_node,
                                         update_scripts=pref.node_viewer.update_scripts,
                                         use_render_mode=False)


class RenderStackNodeGroup(bpy.types.NodeCustomGroup):
    bl_label = 'RenderStack Node Group'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'


classes = [
    RenderStackNodeTree,
    RenderStackNode,
    RenderStackNodeGroup,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
