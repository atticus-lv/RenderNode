import bpy
from RenderStackNode.node_tree import RenderStackNode


def reroute(node):
    def is_task_node(node):
        if node.bl_idname == "RSNodeTaskNode":
            return node
        sub_node = node.inputs[0].links[0].from_node
        return is_task_node(sub_node)

    task_node_name = is_task_node(node)
    return task_node_name


class RSNodeTaskListNode(RenderStackNode):
    '''Render List Node'''
    bl_idname = 'RSNodeTaskListNode'
    bl_label = 'Task List'

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.inputs.new('RSNodeSocketRenderList', "Task")

        self.outputs.new('RSNodeSocketRenderList', 'Task')

    def draw_buttons(self, context, layout):
        try:
            if hasattr(bpy.context.space_data, 'edit_tree'):
                if bpy.context.space_data.edit_tree.nodes.active.name == self.name:
                    row = layout.row(align=1)
                    a = row.operator("rsnode.edit_input", icon='ADD', text='Add')
                    a.socket_type = 'RSNodeSocketRenderList'
                    a.socket_name = 'Task'
                    r = row.operator("rsnode.edit_input", icon='REMOVE', text='Del')
                    r.remove = 1
        except Exception:
            pass



def register():
    bpy.utils.register_class(RSNodeTaskListNode)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskListNode)
