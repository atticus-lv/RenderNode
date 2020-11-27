import json
import bpy
from bpy.props import *

from RenderStackNode.node_tree import RenderStackNode
from RenderStackNode.core.get_tree_info import NODE_TREE


class RenderListNode_OT_GetInfo(bpy.types.Operator):
    bl_idname = "renderlistnode.get_info"
    bl_label = "Get Info"

    data: StringProperty()
    fill_text: BoolProperty(default=False)
    flatten_data: BoolProperty(default=False)

    def execute(self, context):
        nt = NODE_TREE(bpy.context.space_data.edit_tree)
        print(nt.dict)

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
