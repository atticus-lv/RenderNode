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
        self.outputs.new('NodeSocketInt', "Info")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        add = layout.operator("rsnode.edit_input", text="Add Task")
        add.remove = False
        add.socket_type = "RSNodeSocketRenderList"
        add.socket_name  = "Task"

        remove = layout.operator("rsnode.edit_input", text="Remove Unused")
        remove.remove = True


def register():
    bpy.utils.register_class(RSNode_OT_EditInput)
    bpy.utils.register_class(RSNodeRenderListNode)


def unregister():
    bpy.utils.unregister_class(RSNode_OT_EditInput)
    bpy.utils.unregister_class(RSNodeRenderListNode)
