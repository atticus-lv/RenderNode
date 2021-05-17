import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeEeveeRenderSettingsNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeEeveeRenderSettingsNode'
    bl_label = 'Eevee Settings +'

    samples: IntProperty(default=64, min=1, name="Eevee Samples", update=update_node)


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
        task_data['engine'] = "BLENDER_EEVEE"
        task_data['samples'] = self.samples
        return task_data


# def register():
#     bpy.utils.register_class(RSNodeEeveeRenderSettingsNode)
#
#
# def unregister():
#     bpy.utils.unregister_class(RSNodeEeveeRenderSettingsNode)
