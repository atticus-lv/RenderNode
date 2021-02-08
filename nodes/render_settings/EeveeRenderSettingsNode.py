import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeEeveeRenderSettingsNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeEeveeRenderSettingsNode'
    bl_label = 'Eevee Settings'

    samples: IntProperty(default=64, min=1, name="Eevee Samples", update=update_node)

    # data_path: StringProperty(name='Data Path', default='')
    #
    # float_value: FloatProperty(name='Value', update=update_node)
    # string_value: StringProperty(name='Value', update=update_node)
    # bool_value: BoolProperty(name='On', update=update_node)
    # int_value: FloatProperty(name='Value', update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")
        self.width = 175

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0

        layout.prop(self, "samples", text='Samples')

    def get_data(self):
        task_data = {}
        task_data['engine'] = "BLENDER_EEVEE"
        task_data['samples'] = self.samples
        return task_data


def register():
    bpy.utils.register_class(RSNodeEeveeRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeEeveeRenderSettingsNode)
