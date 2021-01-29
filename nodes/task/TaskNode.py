import bpy
from ...nodes.BASE.node_tree import RenderStackNode


class RSNodeTaskNode(RenderStackNode):
    """A simple Task node"""
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")
        self.label = 'task1'

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        layout.prop(self, 'label', text="Label")

        try:
            if hasattr(bpy.context.space_data, 'edit_tree'):
                if bpy.context.space_data.edit_tree.nodes.active.name == self.name:
                    row = layout.row(align=1)
                    a = row.operator("rsnode.edit_input", icon='ADD', text='Add')
                    a.socket_type = 'RSNodeSocketTaskSettings'
                    a.socket_name = "Settings"
                    r = row.operator("rsnode.edit_input", icon='REMOVE', text='Del')
                    r.remove = 1

        except Exception:
            pass


def register():
    bpy.utils.register_class(RSNodeTaskNode)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)
