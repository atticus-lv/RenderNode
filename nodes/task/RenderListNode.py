from bpy.props import *
from ...utility import *
from ...nodes.BASE.node_tree import RenderStackNode


class RSNode_OT_GetInfo(bpy.types.Operator):
    '''left click: get node name
shift:get overwrite details '''
    bl_idname = 'rsn.get_info'
    bl_label = 'get info'

    def invoke(self, context, event):
        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()

        nt = rsn_tree.get_wm_node_tree()
        rsn_task = RSN_Task(node_tree=self.nt,
                            root_node_name=self.render_list_node_name)

        if event.shift:
            for k in nt.node_list_dict.keys():
                print(json.dumps(nt.get_task_data(k), indent=4, ensure_ascii=False))
        else:
            print(json.dumps(nt.node_list_dict, indent=4, ensure_ascii=False))

        return {"FINISHED"}


class RSNodeRenderListNode(RenderStackNode):
    '''Render List Node'''
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    show_process: BoolProperty(name='Show Processor Node')

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")

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
                    # render
                    col = layout.column(align=1)
                    col.scale_y = 1.5

                    col.operator("rsn.render_button",
                                 text=f'Render Confirm').render_list_node_name = self.name
        except Exception:
            pass


def register():
    bpy.utils.register_class(RSNodeRenderListNode)
    bpy.utils.register_class(RSNode_OT_GetInfo)


def unregister():
    bpy.utils.unregister_class(RSNodeRenderListNode)
    bpy.utils.unregister_class(RSNode_OT_GetInfo)
