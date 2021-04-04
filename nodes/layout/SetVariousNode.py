import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import RSN_Nodes


class RSN_OT_SetVarious(bpy.types.Operator):
    bl_idname = 'rsn.set_various'
    bl_label = 'Set Various'

    node_name: StringProperty(default='')
    active: IntProperty(name='Active Var', default=1)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "active")
        layout.separator(factor=0.5)

        col = layout.column(align=1)

        node = context.space_data.edit_tree.nodes[self.node_name]
        for i, input in enumerate(node.inputs):
            if input.is_linked == 1:
                var = input.links[0].from_node
                col.label(text=f"{i + 1} : {var.label if var.label != '' else var.name}")

    def execute(self, context):
        node = context.space_data.edit_tree.nodes[self.node_name]
        node.active = self.active
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


def update_refresh(self, context):
    self.refresh = 0
    self.update()


class RSNodeSetVariousNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeSetVariousNode'
    bl_label = 'Set Various'

    refresh: BoolProperty(default=False, update=update_refresh)

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")
        self.width = 220

    def draw_buttons(self, context, layout):
        pass



def register():
    bpy.utils.register_class(RSN_OT_SetVarious)
    bpy.utils.register_class(RSNodeSetVariousNode)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SetVarious)
    bpy.utils.unregister_class(RSNodeSetVariousNode)
