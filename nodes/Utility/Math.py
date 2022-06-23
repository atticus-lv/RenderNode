import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector

from math import degrees,radians
from math import sin, cos, tan, asin, acos, atan

def update_node(self, context):
    if self.operate_type in {'=', '>', '<'}:
        if self.operate_type == '=': self.create_input('RenderNodeSocketFloat', 'epsilon', 'Epsilon')
        self.create_output('RenderNodeSocketBool', 'bool_output', 'OutBool')
    else:
        self.remove_input('epsilon')
        self.remove_output('bool_output')

    if self.operate_type in {'degrees', 'radians',
                             'sin', 'cos', 'tan', 'asin', 'acos', 'atan'}:
        self.remove_input('value2')
    else:
        self.create_input('RenderNodeSocketFloat', 'value2', 'Value')

    self.execute_tree()


class RenderNodeMath(RenderNodeBase):
    bl_idname = 'RenderNodeMath'
    bl_label = 'Math'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ("", "Function", ""),

            ('+', 'Add', ''),
            ('-', 'Subtract', ''),
            ('*', 'Multiply', ''),
            ('/', 'Divide', ''),

            ('', 'Comparison', ''),

            ('>', 'Greater than', ''),
            ('<', 'Less than', ''),
            ('=', 'Compare', ''),
            ('max', 'Maximum', ''),
            ('min', 'Minimum', ''),

            ('', 'Trigonometric', ''),

            ('sin', 'Sine', ''),
            ('cos', 'Cosine', ''),
            ('tan', 'Tangent', ''),
            None,
            ('asin', 'Arcsin', ''),
            ('acos', 'Arccos', ''),
            ('atan', 'Arctangent', ''),

            ('', 'Conversion', ''),

            ('degrees', 'To Degrees', ''),
            ('radians', 'To Radians', ''),
        ],
        default='+', update=update_node
    )

    def init(self, context):
        self.create_input('RenderNodeSocketFloat', 'value1', 'Value')
        self.create_input('RenderNodeSocketFloat', 'value2', 'Value')
        self.create_output('RenderNodeSocketFloat', 'output', "Output")

    def draw_label(self):
        name = self.bl_rna.properties['operate_type'].enum_items[self.operate_type].name
        return name

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type',text='')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value()

        if self.operate_type in {'+', '-', '*', '/'}:
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(round(eval(f'{s1} {self.operate_type} {s2}'), 2))

        elif self.operate_type in {'degrees', 'radians',
                                   'sin', 'cos', 'tan', 'asin', 'acos', 'atan'}:
            if self.operate_type in {'asin','acos','atan'}:
                s1 = max(-1,min(s1,1))
            self.outputs[0].set_value(eval(f'{self.operate_type}({s1})'))

        elif self.operate_type == '>':
            s2 = self.inputs['value2'].get_value()
            ans = 1 if s1 > s2 else 0
            ans_bool = True if ans == 1 else False
            self.outputs['output'].set_value(ans)
            self.outputs['bool_output'].set_value(ans_bool)

        elif self.operate_type == '<':
            s2 = self.inputs['value2'].get_value()
            ans = 1 if s1 < s2 else 0
            ans_bool = True if s1 < s2 else False
            self.outputs['output'].set_value(ans)
            self.outputs['bool_output'].set_value(ans_bool)

        elif self.operate_type == '=':
            s2 = self.inputs['value2'].get_value()

            e = self.inputs['epsilon'].get_value()
            ans = 1 if abs(s1 - s2) < abs(e) else 0
            ans_bool = True if ans == 1 else False
            self.outputs['output'].set_value(ans)
            self.outputs['bool_output'].set_value(ans_bool)

        elif self.operate_type == 'max':
            s2 = self.inputs['value2'].get_value()
            self.outputs['output'].set_value(max(s1, s2))

        elif self.operate_type == 'min':
            s2 = self.inputs['value2'].get_value()
            self.outputs['output'].set_value(min(s1, s2))


def register():
    bpy.utils.register_class(RenderNodeMath)


def unregister():
    bpy.utils.unregister_class(RenderNodeMath)
