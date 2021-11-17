import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetListIndex(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetListIndex'
    bl_label = 'Get List Index'


    def init(self, context):
        self.create_output('RenderNodeSocketInt', "index", 'Index')

    def process(self,context,id,path):
        node = self.id_data.nodes.get(bpy.context.window_manager.rsn_active_list)
        if not node or node.bl_idname != 'RenderNodeTaskRenderListNode': return
        self.outputs[0].set_value(node.active_index)



def register():
    bpy.utils.register_class(RenderNodeGetListIndex)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetListIndex)
