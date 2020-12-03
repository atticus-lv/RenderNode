import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNode_OT_EditInput(bpy.types.Operator):
    bl_idname = "rsnode.edit_input"
    bl_label = "Add Task"

    remove: BoolProperty(name="remove action", default=False)
    socket_type: StringProperty(default='NodeSocketColor')
    socket_name: StringProperty(default="Input")

    def execute(self, context):
        node_tree = bpy.context.space_data.edit_tree
        active_node = node_tree.nodes.active
        if not self.remove:
            active_node.inputs.new(self.socket_type, self.socket_name)
        else:
            for input in active_node.inputs:
                if not input.is_linked:
                    active_node.inputs.remove(input)

        return {"FINISHED"}


class RSNodeRenderListNode(RenderStackNode):
    '''Render List Node'''
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.inputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.scale_y = 1.25
        row = layout.row(align = True)
        add = row.operator("rsnode.edit_input", text="Task",icon = 'ADD')
        add.remove = False
        add.socket_type = "RSNodeSocketRenderList"
        add.socket_name  = "Task"

        remove = row.operator("rsnode.edit_input", text="Unused",icon ='REMOVE')
        remove.remove = True

        col = layout.box().column(align = False)
        for i, input in enumerate(self.inputs):
            if input.is_linked:
                col.operator("rsn.update_parms",text = f'View Task {i+1}').index = i

        layout.operator("rsn.render_button",text = f'Render')

def register():
    bpy.utils.register_class(RSNode_OT_EditInput)
    bpy.utils.register_class(RSNodeRenderListNode)


def unregister():
    bpy.utils.unregister_class(RSNode_OT_EditInput)
    bpy.utils.unregister_class(RSNodeRenderListNode)
