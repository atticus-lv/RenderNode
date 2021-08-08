import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type in {'JOIN','ADD'}:
        self.remove_input('count')
        self.create_input('RenderNodeSocketString', 'value2', 'Value')
    else:
        self.remove_input('value2')
        self.create_input('RenderNodeSocketInt', 'count', 'Count')

    self.update_parms()


class RenderNodeStringOperate(RenderNodeBase):
    bl_idname = 'RenderNodeStringOperate'
    bl_label = 'String Operate'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('JOIN', 'SubFolder', ''),
            ('ADD', 'Add', ''),
            ('MULTIPLY', 'Muitiply', ''),
        ],
        update=update_node
    )

    def init(self, context):
        self.create_input('RenderNodeSocketString', 'value1', 'Value')
        self.create_input('RenderNodeSocketString', 'value2', 'Value')
        self.create_output('RenderNodeSocketString', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type')

    def process(self):
        s1 = self.inputs['value1'].get_value()

        if self.operate_type == 'ADD':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + s2)
        elif self.operate_type == 'JOIN':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + '/' + s2)
        else:
            s2 = self.inputs['count'].get_value()
            self.outputs[0].set_value(s1 * s2)


def register():
    bpy.utils.register_class(RenderNodeStringOperate)


def unregister():
    bpy.utils.unregister_class(RenderNodeStringOperate)
