import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RS_OT_ChangeSamples(bpy.types.Operator):
    """Change the samples"""
    bl_idname = "rsn.change_samples"
    bl_label = "Change Samples"

    scale: FloatProperty(default=1)
    node_name: StringProperty()

    def execute(self, context):
        node = context.space_data.edit_tree.nodes[self.node_name]
        node.samples *= self.scale

        return {"FINISHED"}


class RSNodeCyclesRenderSettingsNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeCyclesRenderSettingsNode'
    bl_label = 'Cycles Settings'

    samples: IntProperty(default=128, min=1, name="Cycles Samples", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, "samples", text='Samples')

        row = col.row(align=1)
        half = row.operator("rsn.change_samples", text="Half")
        half.node_name = self.name
        half.scale = 0.5

        double = row.operator("rsn.change_samples", text="Double")
        double.node_name = self.name
        double.scale = 2

    def get_data(self):
        task_data = {}
        task_data['engine'] = "CYCLES"
        task_data['samples'] = self.samples
        return task_data


def register():
    bpy.utils.register_class(RS_OT_ChangeSamples)
    bpy.utils.register_class(RSNodeCyclesRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RS_OT_ChangeSamples)
    bpy.utils.unregister_class(RSNodeCyclesRenderSettingsNode)
