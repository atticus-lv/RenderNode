import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import RSN_Nodes


class RSN_OT_SetVarious(bpy.types.Operator):
    bl_idname = 'rsn.set_various'
    bl_label = 'Set Various'


    node_name: StringProperty(default='')
    active: IntProperty(name = 'Active Var',default=1)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "active")
        layout.separator(factor=0.5)

        col = layout.column(align=1)

        node = context.space_data.edit_tree.nodes[self.node_name]
        for i, input in enumerate(node.inputs):
            if input.is_linked == 1:
                var = input.links[0].from_node
                col.label(text=f"{i + 1} : {var.name}")

    def execute(self, context):
        node = context.space_data.edit_tree.nodes[self.node_name]
        node.active = self.active
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

def update_refresh(self,context):
    self.refresh = 0
    self.update()

class RSNodeSetVariousNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeSetVariousNode'
    bl_label = 'Set Various'

    refresh:BoolProperty(default=False,update=update_refresh)
    node_list: StringProperty(default='')

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")
        self.width = 220

    def draw_buttons(self, context, layout):
        layout.prop(self, "refresh", icon="FILE_REFRESH")
        layout.separator(factor = 0.5)
        col = layout.column()
        if self.node_list != '':
            nodes = self.node_list.split(',')
            for node_name in nodes:
                node = context.space_data.edit_tree.nodes[node_name]
                row = col.row()
                row.prop(node,"name")
                # row.prop(node, 'active', text='Various')
                row.operator("rsn.set_various",text="",icon="SETTINGS").node_name = node.name

    def update(self):
        self.get_var_nodes()

    def get_var_nodes(self):
        nt = bpy.context.space_data.edit_tree
        RSN = RSN_Nodes(node_tree=nt, root_node_name=self.name)
        nodes = RSN.get_children_from_node(root_node=self)
        self.node_list = ','.join(
            [node_name for node_name in nodes if nt.nodes[node_name].bl_idname == "RSNodeVariousNode"])


def register():
    bpy.utils.register_class(RSN_OT_SetVarious)
    bpy.utils.register_class(RSNodeSetVariousNode)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SetVarious)
    bpy.utils.unregister_class(RSNodeSetVariousNode)
