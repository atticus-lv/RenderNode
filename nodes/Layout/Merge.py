import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from ...nodes.BASE._runtime import runtime_info


class RenderNodeMerge(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeMerge'
    bl_label = 'Merge'

    def init(self, context):
        self.create_input('RSNodeSocketTaskSettings', 'Input', 'Input')
        self.create_output('RSNodeSocketTaskSettings', 'Output', 'Output')

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Input")


def register():
    bpy.utils.register_class(RenderNodeMerge)


def unregister():
    bpy.utils.unregister_class(RenderNodeMerge)
