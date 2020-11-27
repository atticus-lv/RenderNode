import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeTaskNode(RenderStackNode):
    '''A simple Task node'''
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    task_name:StringProperty(name = "Task Name",default="Task")

    def init(self, context):
        self.inputs.new('RSNodeSocketCameraSettings', "Camera Settings")
        self.inputs.new('RSNodeSocketRenderSettings', "Render Settings")
        self.inputs.new('RSNodeSocketOutputSettings', "Output Settings")

        self.outputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'task_name')
        pass

    def draw_label(self):
        return self.task_name



def register():
    bpy.utils.register_class(RSNodeTaskNode)

def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)
