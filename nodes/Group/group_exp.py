import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from ...nodes.BASE.node_tree import RenderStackNodeTree




class RenderNodeGroupExp(bpy.types.NodeCustomGroup, RenderStackNodeTree):
    bl_idname = 'RenderNodeGroupExp'
    bl_label = 'Group Exp'
    bl_icon = 'OUTLINER_OB_EMPTY'

    group_name = StringProperty()

    def init(self, context):

        self.node_tree = bpy.data.node_groups.new('nooobgroup', 'RenderStackNodeTree')
        self.group_name = self.node_tree.name
        # self.node_tree.parent = self
        # space = context.space_data
        # nodes = self.node_tree.nodes
        #
        # inputnode = nodes.new('SvGroupInputsNode')
        # outputnode = nodes.new('SvGroupOutputsNode')
        # inputnode.location = (-300, 0)
        # outputnode.location = (300, 0)

def register():
    bpy.utils.register_class(RenderNodeGroupExp)


def unregister():
    bpy.utils.unregister_class(RenderNodeGroupExp)