import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeCyclesRenderSettingsNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeCyclesRenderSettingsNode'
    bl_label = 'Cycles Settings'

    samples: IntProperty(default=128, min=1, name="Cycles Samples", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, "samples", text='Samples')

    def draw_buttons_ext(self, context, layout):
        pass


def register():
    bpy.utils.register_class(RSNodeCyclesRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCyclesRenderSettingsNode)
