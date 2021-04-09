import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import *


class VariousNodeProperty(bpy.types.PropertyGroup):
    name: StringProperty()
    active: IntProperty(default=1, min=1)


class VariousCollectList(bpy.types.PropertyGroup):
    name: StringProperty(default='Collect 1')
    use_for_render: BoolProperty(default=True)
    node_properties: CollectionProperty(name="Node Property", type=VariousNodeProperty)


class RSN_UL_TaskVarCollectList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            pass
        elif self.layout_type in {'GRID'}:
            pass

        row = layout.row(align=True)
        row.prop(item, "name", text="", emboss=False, icon_value=icon)
        row.prop(item, "use_for_render", text="", icon="CHECKMARK")


class RSN_OT_AddVarCollect(bpy.types.Operator):
    bl_idname = "rsn.add_var_collect"
    bl_label = "Add Var Collect"

    task_node_name: StringProperty(default='')
    node = None

    def execute(self, context):
        self.node = context.space_data.edit_tree.nodes[self.task_node_name]
        self.node.var_collect_list.add()
        self.node.var_collect_list_index = len(self.node.var_collect_list) - 1
        self.get_var_nodes()
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


class RSN_OT_RemoveVarCollect(bpy.types.Operator):
    bl_idname = "rsn.remove_var_collect"
    bl_label = "Remove Var Collect"

    task_node_name: StringProperty(default='')

    def execute(self, context):
        node = context.space_data.edit_tree.nodes[self.task_node_name]
        node.var_collect_list.remove(node.var_collect_list_index)
        node.var_collect_list_index -= 1 if node.var_collect_list_index != 0 else 0
        return {"FINISHED"}


def update_node(self, context):
    if len(self.var_collect_list) != 0:
        self.update_parms()
    self.update_parms()


class RSNodeTaskNode(RenderStackNode):
    """A simple Task node"""
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
        layout.label(text="Various Collect:")
        row = layout.row()
        row.template_list(
            "RSN_UL_TaskVarCollectList", "The list",
            self, "var_collect_list",
            self, "var_collect_list_index", )

        col = row.column(align=1)
        col.operator("rsn.add_var_collect", text="", icon="ADD").task_node_name = self.name
        col.operator("rsn.remove_var_collect", text="", icon="REMOVE").task_node_name = self.name

        layout.label(text="Current Various Node:")
        col = layout.column(align=0)
        if len(self.var_collect_list) != 0:
            curr_var_collect = self.var_collect_list[self.var_collect_list_index]
            for item in curr_var_collect.node_properties:
                col.prop(item, 'active', text=item.name)

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
        except:
            return {"CANCELLED"}


def register():
    bpy.utils.register_class(VariousNodeProperty)
    bpy.utils.register_class(VariousCollectList)
    bpy.utils.register_class(RSN_UL_TaskVarCollectList)

    bpy.utils.register_class(RSN_OT_AddVarCollect)
    bpy.utils.register_class(RSN_OT_RemoveVarCollect)

    bpy.utils.register_class(RSN_OT_GetTaskInfo)
    bpy.utils.register_class(RSNodeTaskNode)


def unregister():
    bpy.utils.unregister_class(VariousNodeProperty)
    bpy.utils.unregister_class(VariousCollectList)
    bpy.utils.unregister_class(RSN_UL_TaskVarCollectList)

    bpy.utils.unregister_class(RSN_OT_AddVarCollect)
    bpy.utils.unregister_class(RSN_OT_RemoveVarCollect)

    bpy.utils.unregister_class(RSN_OT_GetTaskInfo)
    bpy.utils.unregister_class(RSNodeTaskNode)
