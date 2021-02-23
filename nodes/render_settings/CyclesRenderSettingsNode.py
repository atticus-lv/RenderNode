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
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        layout.prop(self, "samples", text='Samples')

    def get_data(self):
        task_data = {}
        task_data['engine'] = "CYCLES"
        task_data['samples'] = self.samples
        return task_data


def register():
    bpy.utils.register_class(RSNodeCyclesRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCyclesRenderSettingsNode)
