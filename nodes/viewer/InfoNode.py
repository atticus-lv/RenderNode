import json
import bpy
from bpy.props import *

from RenderStackNode.node_tree import RenderStackNode
from RenderStackNode.core.get_tree_info import get_node_list, separate_nodes


class RenderListNode_OT_GetInfo(bpy.types.Operator):
    bl_idname = "renderlistnode.get_info"
    bl_label = "Get Info"

    data: StringProperty()
    fill_text: BoolProperty(default=False)
    flatten_data: BoolProperty(default=False)

    def get_data(self):
        nt = bpy.context.space_data.edit_tree
        nodes = get_node_list(nt.nodes.active)
        print(nodes)
        dict = separate_nodes(nodes)
        return dict

    def execute(self, context):
        print(self.get_data())

        return {"FINISHED"}


class RSNodeInfoNode(RenderStackNode):
    bl_idname = 'RSNodeRenderInfoNode'
    bl_label = 'Info'

    def init(self, context):
        self.inputs.new('NodeSocketString', "Info")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.operator("renderlistnode.get_info").fill_text = 1


def register():
    bpy.utils.register_class(RenderListNode_OT_GetInfo)
    bpy.utils.register_class(RSNodeInfoNode)


def unregister():
    bpy.utils.unregister_class(RenderListNode_OT_GetInfo)
    bpy.utils.unregister_class(RSNodeInfoNode)
