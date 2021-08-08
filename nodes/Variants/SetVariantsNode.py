import bpy
from bpy.props import *
from ..BASE.node_base import RenderNodeBase
from ...utility import *


def update_node(self, context):
    if not self.use: return None
    task_node = context.space_data.node_tree.nodes.get(bpy.context.window_manager.rsn_viewer_node)
    if task_node: task_node.update()


class VariantsNodeProperty(bpy.types.PropertyGroup):
    name: StringProperty(name="The name of the variants node")
    active: IntProperty(default=0, min=0, name="Active Input",update=update_node)
    use: BoolProperty(default=True, name="Use for render",
                      description="If enable, the active input of the variant node will be apply to the Scene,else it will apply the last input of the variant node")


# use uilist for visualization
class RSN_UL_VarCollectNodeList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        sub = layout.split(align=True, factor=0.5)

        sub.label(text=item.name, icon="RADIOBUT_OFF")
        row = sub.row()
        row.prop(item, "active", text="Active")
        row.prop(item, "use", text="", icon="CHECKMARK")


class RSN_OT_UpdateVarCollect(bpy.types.Operator):
    """ADD/REMOVE List item"""
    bl_idname = "rsn.update_var_collect"
    bl_label = "Update Collect"

    action: EnumProperty(name="Edit", items=[('ADD', 'Add', ''), ('REMOVE', 'Remove', '')])

    sort: BoolProperty(name="Sort", description="Sort when update collect", default=True)

    node_name: StringProperty(default='')
    node = None

    def execute(self, context):
        self.node = context.space_data.edit_tree.nodes[self.node_name]
        if self.action == "ADD":
            self.get_var_nodes()
            self.node.node_collect_index = len(self.node.node_collect) - 1

            if self.sort:
                self.sort_items()

        return {"FINISHED"}

    def get_var_nodes(self):
        nt = bpy.context.space_data.edit_tree

        RSN = RSN_Nodes(node_tree=nt, root_node_name=self.node.name)
        nodes = RSN.get_children_from_node(root_node=self.node)
        node_list = ','.join(
            [node_name for node_name in nodes if nt.nodes[node_name].bl_idname == "RSNodeVariantsNode"])

        for i, src_node in enumerate(self.node.node_collect.keys()):
            if src_node not in node_list.split(','):
                self.node.node_collect.remove(i)
                self.node.node_collect_index -= 1 if self.node.node_collect_index != 0 else 0

        for node_name in node_list.split(','):
            if node_name != '' and node_name not in self.node.node_collect.keys():
                prop = self.node.node_collect.add()
                prop.name = node_name
                prop.active = 0

    def sort_items(self):
        item_list = [{"name": k, "value": v.active} for k, v in self.node.node_collect.items()]

        sort_list = sorted(item_list, key=lambda x: x["name"])

        self.node.node_collect.clear()

        for i, item in enumerate(sort_list):
            prop = self.node.node_collect.add()
            prop.name = item_list[i]["name"]
            prop.active = item_list[i]["value"]


class RSNodeSetVariantsNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodeSetVariantsNode'
    bl_label = 'Set Variants'

    node_list = None

    node_collect: CollectionProperty(name="Node Property", type=VariantsNodeProperty)
    node_collect_index: IntProperty(default=0)

    sort: BoolProperty(name="Sort", description="Sort when update collect", default=True)

    def init(self, context):
        self.width = 220
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.template_list(
            "RSN_UL_VarCollectNodeList", "The list",
            self, "node_collect",
            self, "node_collect_index", )

        row = layout.row(align=1)
        edit = row.operator("rsn.update_var_collect", icon="FILE_REFRESH")
        edit.action = "ADD"
        edit.node_name = self.name
        edit.sort = self.sort

        row.prop(self, "sort", icon='SORTSIZE', text='')

    def get_data(self):
        pass


def register():
    bpy.utils.register_class(VariantsNodeProperty)
    bpy.utils.register_class(RSN_UL_VarCollectNodeList)

    bpy.utils.register_class(RSN_OT_UpdateVarCollect)

    bpy.utils.register_class(RSNodeSetVariantsNode)


def unregister():
    bpy.utils.unregister_class(VariantsNodeProperty)
    bpy.utils.unregister_class(RSN_UL_VarCollectNodeList)

    bpy.utils.unregister_class(RSN_OT_UpdateVarCollect)

    bpy.utils.unregister_class(RSNodeSetVariantsNode)
