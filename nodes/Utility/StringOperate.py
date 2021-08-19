import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type == 'MULTIPLY':
        self.create_input('RenderNodeSocketInt', 'count', 'Count')
    else:
        self.remove_input('count')
        self.create_input('RenderNodeSocketString', 'value2', 'Value')

    if self.operate_type in {'JOIN', 'ADD'}:
        self.create_input('RenderNodeSocketString', 'value2', 'Value')
    else:
        self.remove_input('value2')

    if self.operate_type == 'REPLACE':
        self.create_input('RenderNodeSocketString', 'replace_old', 'Old')
        self.create_input('RenderNodeSocketString', 'replace_new', 'New')
    else:
        self.remove_input('replace_old')
        self.remove_input('replace_new')

    if self.operate_type == 'TEXT_2_STR':
        self.remove_input('value1')
        self.create_input('RenderNodeSocketText', 'text', 'Text')
    else:
        self.remove_input('text')
        self.create_input('RenderNodeSocketString', 'value1', 'Value')

    self.execute_tree()


class RenderNodeStringOperate(RenderNodeBase):
    bl_idname = 'RenderNodeStringOperate'
    bl_label = 'String Operate'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('', 'Combine', ''),

            ('JOIN', 'Join Path', ''),
            ('ADD', 'Add', ''),
            ('MULTIPLY', 'Multiply', ''),

            ('', 'Conversion', ''),
            ('REPLACE', 'Replace', ''),
            ('TEXT_2_STR', 'Text to String', ''),
        ],
        update=update_node,
        default='JOIN'
    )

    def init(self, context):
        self.create_input('RenderNodeSocketString', 'value1', 'Value')
        self.create_input('RenderNodeSocketString', 'value2', 'Value')
        self.create_output('RenderNodeSocketString', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value() if 'value1' in self.inputs else None

        if self.operate_type == 'ADD':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + s2)

        elif self.operate_type == 'JOIN':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + '/' + s2)

        elif self.operate_type == 'MULTIPLY':
            s2 = self.inputs['count'].get_value()
            self.outputs[0].set_value(s1 * s2)

        elif self.operate_type == 'REPLACE':
            old = self.inputs['replace_old'].get_value()
            new = self.inputs['replace'].get_value()
            res = s1.replace(old, new)
            self.outputs[0].set_value(res)

        elif self.operate_type == 'TEXT_2_STR':
            res = None
            text = self.inputs['text'].get_value()
            if text:
                res = text.as_string()
            self.outputs[0].set_value(res)


def register():
    bpy.utils.register_class(RenderNodeStringOperate)


def unregister():
    bpy.utils.unregister_class(RenderNodeStringOperate)
