import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RenderNodeMath(RenderNodeBase):
    bl_idname = 'RenderNodeMath'
    bl_label = 'Math'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('+', 'Add', ''),
            ('-', 'Subtract', ''),
            ('*', 'Muitiply', ''),
            ('/', 'Divide', ''),
        ],
        default='+', update=update_node
    )

    def init(self, context):
        self.create_input('RenderNodeSocketFloat', 'value1', 'Value')
        self.create_input('RenderNodeSocketFloat', 'value2', 'Value')
        self.create_output('RenderNodeSocketFloat', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type')

    def process(self):
        s1 = self.inputs['value1'].get_value()
        s2 = self.inputs['value2'].get_value()

        self.outputs[0].set_value(round(eval(f'{s1} {self.operate_type} {s2}'), 2))


def register():
    bpy.utils.register_class(RenderNodeMath)


def unregister():
    bpy.utils.unregister_class(RenderNodeMath)
