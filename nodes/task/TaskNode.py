import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeTaskNode(RenderStackNode):
    '''A simple Task node'''
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    task_name: StringProperty(name="Task Name", default="Task")

    def init(self, context):
        self.inputs.new('RSNodeSocketCamera', "Camera")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'task_name', text="$task")

    def draw_label(self):
        return self.name

    def draw_buttons_ext(self, context, layout):
        add = layout.operator("rsnode.edit_input", text="Add Settings")
        add.remove = False
        add.socket_type = "RSNodeSocketTaskSettings"
        add.socket_name = "Settings"


        remove = layout.operator("rsnode.edit_input", text="Remove Unused")
        remove.remove = True



def register():
    bpy.utils.register_class(RSNodeTaskNode)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)
