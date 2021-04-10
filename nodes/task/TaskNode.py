import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import *


class VariousNodeProperty(bpy.types.PropertyGroup):
    name: StringProperty()
    active: IntProperty(default=1, min=1)


class VariousCollectList(bpy.types.PropertyGroup):
    name: StringProperty(default='Var Collect')
    use_for_render: BoolProperty(default=True)
    node_properties: CollectionProperty(name="Node Property", type=VariousNodeProperty)
    node_properties_index: IntProperty(default=0)


class RSN_UL_TaskVarCollectList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.prop(item, "name", text="", emboss=False, icon_value=icon)
        row.prop(item, "use_for_render", text="", icon="CHECKMARK")


class RSN_UL_VarCollectNodeList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(text=item.name)
        row.prop(item, "active", text="Active")


class RSN_OT_EditVarCollect(bpy.types.Operator):
    """ADD/REMOVE List item"""
    bl_idname = "rsn.edit_var_collect"
    bl_label = "Edit Var Collect"

    action: EnumProperty(name="Edit", items=[('ADD', 'Add', ''), ('REMOVE', 'Remove', '')])

    task_node_name: StringProperty(default='')
    node = None

    def execute(self, context):
        self.node = context.space_data.edit_tree.nodes[self.task_node_name]
        if self.action == "ADD":

            self.node.var_collect_list.add()
            self.node.var_collect_list_index = len(self.node.var_collect_list) - 1
            self.get_var_nodes()
        else:

            self.node.var_collect_list.remove(self.node.var_collect_list_index)
            self.node.var_collect_list_index -= 1 if self.node.var_collect_list_index != 0 else 0
        return {"FINISHED"}

    def get_var_nodes(self):
        nt = bpy.context.space_data.edit_tree
        current_item = self.node.var_collect_list[self.node.var_collect_list_index]

        RSN = RSN_Nodes(node_tree=nt, root_node_name=self.node.name)
        nodes = RSN.get_children_from_node(root_node=self.node)
        node_list = ','.join(
            [node_name for node_name in nodes if nt.nodes[node_name].bl_idname == "RSNodeVariousNode"])

        for node_name in node_list.split(','):
            if node_name != '' and node_name not in current_item.node_properties.keys():
                prop = current_item.node_properties.add()
                prop.name = node_name
                prop.active = 1


def update_node(self, context):
    if len(self.var_collect_list) != 0:
        self.update_parms()


class RSNodeTaskNode(RenderStackNode):
    """A simple Task node
    :parm node_list: for checking update of various nodes
    """
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    node_list = None

    var_collect_list: CollectionProperty(name="Var Collect", type=VariousCollectList)
    var_collect_list_index: IntProperty(default=0, min=0, update=update_node)

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")
        self.label = self.name

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0

        row = layout.row(align=1)
        row.prop(self, 'label', text='')
        row.operator("rsn.get_task_info", text="", icon="INFO").task_name = self.name

    def draw_buttons_ext(self, context, layout):
        # Various Collect List
        layout.label(text="Various Collect:")
        row = layout.row(align=1)
        row.template_list(
            "RSN_UL_TaskVarCollectList", "The list",
            self, "var_collect_list",
            self, "var_collect_list_index", )

        # edit items bUtton
        col = row.column(align=1)
        # Add item
        ADD = col.operator("rsn.edit_var_collect", text="", icon="ADD")
        ADD.task_node_name = self.name
        ADD.action = "ADD"
        # Remove item
        REMOVE = col.operator("rsn.edit_var_collect", text="", icon="REMOVE")
        REMOVE.task_node_name = self.name
        REMOVE.action = "REMOVE"

        # Current Various Collect
        layout.label(text="Current Various Collect:")
        if len(self.var_collect_list) != 0:
            curr_var_collect = self.var_collect_list[self.var_collect_list_index]
            row = layout.row(align=1)
            row.template_list(
                "RSN_UL_VarCollectNodeList", "The list",
                curr_var_collect, "node_properties",
                curr_var_collect, "node_properties_index", )

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
    bpy.utils.register_class(VariousNodeProperty)
    bpy.utils.register_class(VariousCollectList)

    bpy.utils.register_class(RSN_UL_TaskVarCollectList)
    bpy.utils.register_class(RSN_UL_VarCollectNodeList)

    bpy.utils.register_class(RSN_OT_EditVarCollect)

    bpy.utils.register_class(RSN_OT_GetTaskInfo)
    bpy.utils.register_class(RSNodeTaskNode)


def unregister():
    bpy.utils.unregister_class(VariousNodeProperty)
    bpy.utils.unregister_class(VariousCollectList)

    bpy.utils.unregister_class(RSN_UL_TaskVarCollectList)
    bpy.utils.unregister_class(RSN_UL_VarCollectNodeList)

    bpy.utils.unregister_class(RSN_OT_EditVarCollect)

    bpy.utils.unregister_class(RSN_OT_GetTaskInfo)
    bpy.utils.unregister_class(RSNodeTaskNode)
