import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import *





def update_node(self, context):
    if len(self.var_collect_list) != 0:
        self.update_parms()


class RSNodeTaskNode(RenderStackNode):
    """A simple Task node
    :parm node_list: for checking update of various nodes
    """
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'


    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")
        self.label = self.name

        # bpy.ops.rsn.edit_var_collect(action="ADD", task_node_name=self.name)

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0

        row = layout.row(align=1)
        row.prop(self, 'label', text='')
        row.operator("rsn.get_task_info", text="", icon="INFO").task_name = self.name

    def draw_buttons_ext(self, context, layout):
        pass
        # Various Collect List
        # layout.label(text="Various Collect:")
        # row = layout.row(align=1)
        # row.template_list(
        #     "RSN_UL_TaskVarCollectList", "The list",
        #     self, "var_collect_list",
        #     self, "var_collect_list_index", )
        #
        # # edit items bUtton
        # col = row.column(align=1)
        # # Add item
        # ADD = col.operator("rsn.edit_var_collect", text="", icon="ADD")
        # ADD.task_node_name = self.name
        # ADD.action = "ADD"
        # # Remove item
        # REMOVE = col.operator("rsn.edit_var_collect", text="", icon="REMOVE")
        # REMOVE.task_node_name = self.name
        # REMOVE.action = "REMOVE"
        #
        # # Current Various Collect
        # layout.label(text="Current Various Collect:")
        # if len(self.var_collect_list) != 0:
        #     curr_var_collect = self.var_collect_list[self.var_collect_list_index]
        #     row = layout.row(align=1)
        #     row.template_list(
        #         "RSN_UL_VarCollectNodeList", "The list",
        #         curr_var_collect, "node_properties",
        #         curr_var_collect, "node_properties_index", )

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Settings")

    def get_data(self):
        var_collect_data = {}
        # var_collect_data['active_index'] = self.var_collect_list_index

        for i, collect in enumerate(self.var_collect_list):
            var_nodes = {}
            for item in collect.node_properties:
                var_nodes[item.name] = item.active

            var_collect_data[i] = var_nodes

        return var_collect_data


class RSN_OT_GetTaskInfo(bpy.types.Operator):
    """Information"""
    bl_idname = "rsn.get_task_info"
    bl_label = "Information"

    task_name: StringProperty(default='')
    task_data: StringProperty(default='')

    def execute(self, context):
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        row = layout.split(factor=0.3, align=1)
        row.operator('rsn.clip_board', text='Copy').data_to_copy = self.task_data
        row.label(text='')

        col = layout.box().column(align=1)
        if self.task_data != '':
            l = self.task_data.split('\n')
            for s in l:
                col.label(text=s)

    def invoke(self, context, event):
        nt = context.space_data.edit_tree
        RSN = RSN_Nodes(node_tree=nt, root_node_name=self.task_name)
        try:
            task_dict = RSN.get_children_from_task(task_name=self.task_name, return_dict=True)
            data = RSN.get_task_data(task_name=self.task_name, task_dict=task_dict)
            self.task_data = json.dumps(data, indent=2, ensure_ascii=False)
            return context.window_manager.invoke_popup(self, width=300)
        except Exception:
            return {"CANCELLED"}


def register():


    bpy.utils.register_class(RSN_OT_GetTaskInfo)
    bpy.utils.register_class(RSNodeTaskNode)


def unregister():


    bpy.utils.unregister_class(RSN_OT_GetTaskInfo)
    bpy.utils.unregister_class(RSNodeTaskNode)
