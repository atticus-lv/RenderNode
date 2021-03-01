import bpy
from ...nodes.BASE.node_tree import RenderStackNode


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
        layout.prop(self, 'label', text="Label")

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Settings")


def register():
    bpy.utils.register_class(RSNodeTaskNode)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)
