import bpy
import json
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import *


class RSNodeTaskNode(RenderStackNode):
    """A simple Task node"""
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")
        self.label = self.name

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0

        row = layout.row(align=1)
        row.prop(self, 'label', text='')
        row.operator("rsn.get_task_info", text="", icon="INFO").task_name = self.name

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Settings")


class RSN_OT_GetTaskInfo(bpy.types.Operator):
    """Information"""
    bl_idname = "rsn.get_task_info"
    bl_label = "Information"

    task_name: StringProperty(default='')
    task_data: StringProperty(default='')

    def execute(self, context):
        return {"FINISHED"}

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
        nt = context.space_data.edit_tree
        RSN = RSN_Nodes(node_tree=nt, root_node_name=self.task_name)

        task_dict = RSN.get_children_from_task(task_name=self.task_name, return_dict=True)
        data = RSN.get_task_data(task_name=self.task_name, task_dict=task_dict)
        self.task_data = json.dumps(data, indent=2, ensure_ascii=False)
        return context.window_manager.invoke_popup(self, width=300)


def register():
    bpy.utils.register_class(RSNodeTaskNode)
    bpy.utils.register_class(RSN_OT_GetTaskInfo)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)
    bpy.utils.unregister_class(RSN_OT_GetTaskInfo)
