import json
import bpy
from bpy.props import *
from RenderStackNode.utility import NODE_TREE
from RenderStackNode.node_tree import RenderStackNode

class RSNode_OT_GetInfo(bpy.types.Operator):
    '''left click: get node name
shift:get overwrite details '''
    bl_idname = 'rsn.get_info'
    bl_label = 'get info'

    def invoke(self, context,event):
        nt = NODE_TREE(context.space_data.edit_tree)
        if event.shift:
            for k in nt.dict.keys():
                print(json.dumps(nt.get_task_data(k), indent=4, ensure_ascii=False))
        else:
            print(json.dumps(nt.dict, indent=4, ensure_ascii=False))

        return {"FINISHED"}


class RSNodeRenderListNode(RenderStackNode):
    '''Render List Node'''
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "render")
        self.inputs.new('RSNodeSocketRenderList', "render")
        self.inputs.new('RSNodeSocketRenderList', "render")
        self.inputs.new('RSNodeSocketRenderList', "render")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.operator("rsn.get_info", text=f'Print Info (Console)')
        box = layout.box()
        box.scale_y = 1.5
        box.operator("rsn.render_button",text = f'Render Inputs')


def register():
    bpy.utils.register_class(RSNodeRenderListNode)
    bpy.utils.register_class(RSNode_OT_GetInfo)


def unregister():
    bpy.utils.unregister_class(RSNodeRenderListNode)
    bpy.utils.unregister_class(RSNode_OT_GetInfo)
