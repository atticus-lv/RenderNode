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

        self.outputs.new('RSNodeSocketRenderList', 'render')

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        # edit inputs
        layout.scale_y = 1.25
        row = layout.row(align=True)
        add = row.operator("rsnode.edit_input", text="Task", icon='ADD')
        add.remove = False
        add.socket_type = "RSNodeSocketRenderList"
        add.socket_name = "Task"

        remove = row.operator("rsnode.edit_input", text="Unused", icon='REMOVE')
        remove.remove = True
        # view input task name
        if context.window_manager.rsn_viewer_modal is False:
            col = layout.box().column(align=False)
            for i, input in enumerate(self.inputs):
                if input.is_linked:
                    node = reroute(input.links[0].from_node)
                    col.operator("rsn.update_parms", text=f'View {node.name}').task_name = node.name
        else:
            layout.label(text='Using Viewer Node')


def register():
    bpy.utils.register_class(RSNodeTaskListNode)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskListNode)
