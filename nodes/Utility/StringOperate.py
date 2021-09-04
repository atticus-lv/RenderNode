import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type == 'TEXT_2_STR':
        self.remove_input('value1')
        self.create_input('RenderNodeSocketText', 'text', 'Text')
    else:
        self.remove_input('text')
        self.create_input('RenderNodeSocketString', 'value1', 'Value')

    if self.operate_type == 'INT_2_STR':
        self.remove_input('value1')
        self.create_input('RenderNodeSocketInt', 'int', 'Int')
    else:
        self.remove_input('int')
        self.create_input('RenderNodeSocketString', 'value1', 'Value')

    if self.operate_type == 'STR_2_INT':
        self.remove_output('output')
        self.create_output('RenderNodeSocketInt', 'int', 'Int')
    else:
        self.remove_output('int')
        self.create_output('RenderNodeSocketString', 'output', 'Output')

    if self.operate_type == 'MULTIPLY':
        self.create_input('RenderNodeSocketInt', 'count', 'Count')
    else:
        self.remove_input('count')
        self.create_input('RenderNodeSocketString', 'value2', 'Value')

    if self.operate_type in {'SUB','JOIN', 'SPACE', 'DOT', 'UNDERSCORE'}:
        self.create_input('RenderNodeSocketString', 'value2', 'Value')
    else:
        self.remove_input('value2')

    if self.operate_type == 'REPLACE':
        self.create_input('RenderNodeSocketString', 'replace_old', 'Old')
        self.create_input('RenderNodeSocketString', 'replace_new', 'New')
    else:
        self.remove_input('replace_old')
        self.remove_input('replace_new')

    if self.operate_type == 'SLICE':
        self.create_input('RenderNodeSocketString', 'value1', 'Value')
        self.create_input('RenderNodeSocketInt', 'slice_from', 'From')
        self.create_input('RenderNodeSocketInt', 'slice_to', 'To')
    else:
        self.remove_input('slice_from')
        self.remove_input('slice_to')

    if self.operate_type in {'ABS', 'REL'}:
        pass

    self.execute_tree()


class RenderNodeStringOperate(RenderNodeBase):
    bl_idname = 'RenderNodeStringOperate'
    bl_label = 'String Operate'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('', 'Concat', ''),
            ('JOIN', 'Join', ''),
            ('SPACE', 'Space', ''),
            ('DOT', 'Dot', ''),
            ('UNDERSCORE', 'Underscore', ''),

            ('', 'Function', ''),
            ('REPLACE', 'Replace', ''),
            ('MULTIPLY', 'Multiply', ''),
            ('SLICE', 'Slice', ''),

            ('', 'Path', ''),
            ('SUB', 'Join Path', ''),
            ('ABS', 'Abs Path', ''),
            ('REL', 'Rel Path', ''),

            ('', 'Conversion', ''),
            ('INT_2_STR', 'Int to String', ''),
            ('STR_2_INT', 'String to Int', ''),
            ('TEXT_2_STR', 'Text to String', ''),
        ],
        update=update_node,
        default='SUB'
    )

    def init(self, context):
        self.create_input('RenderNodeSocketString', 'value1', 'Value')
        self.create_input('RenderNodeSocketString', 'value2', 'Value')
        self.create_output('RenderNodeSocketString', 'output', "Output")

    def draw_label(self):
        name = self.bl_rna.properties['operate_type'].enum_items[self.operate_type].name
        return name

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value() if 'value1' in self.inputs else None

        if self.operate_type == 'JOIN':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + s2)

        elif self.operate_type == 'SUB':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + '/' + s2)

        elif self.operate_type == 'REL':
            self.outputs[0].set_value(bpy.path.relpath(s1))

        elif self.operate_type == 'ABS':
            self.outputs[0].set_value(bpy.path.abspath(s1))

        elif self.operate_type == 'SPACE':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + ' ' + s2)

        elif self.operate_type == 'DOT':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + '.' + s2)

        elif self.operate_type == 'UNDERSCORE':
            s2 = self.inputs['value2'].get_value()
            self.outputs[0].set_value(s1 + '_' + s2)

        elif self.operate_type == 'MULTIPLY':
            s2 = self.inputs['count'].get_value()
            self.outputs[0].set_value(s1 * s2)

        elif self.operate_type == 'REPLACE':
            old = self.inputs['replace_old'].get_value()
            new = self.inputs['replace_new'].get_value()
            res = s1.replace(old, new)
            self.outputs[0].set_value(res)

        elif self.operate_type == 'SLICE':
            from_id = self.inputs['slice_from'].get_value()
            to_id = self.inputs['slice_to'].get_value()

            try:
                res = s1[from_id:to_id]
            except IndexError:
                res = None

            self.outputs[0].set_value(res)

        elif self.operate_type == 'TEXT_2_STR':
            res = None
            text = self.inputs['text'].get_value()
            if text:
                res = text.as_string()
            self.outputs[0].set_value(res)

        elif self.operate_type == 'INT_2_STR':
            res = None
            i = self.inputs['int'].get_value()
            if i is not None:
                res = str(i)
            self.outputs[0].set_value(res)

        elif self.operate_type == 'STR_2_INT':
            s = self.inputs['value1'].get_value()
            try:
                ans = int(s)
            except:
                ans = 0
            self.outputs[0].set_value(ans)


def register():
    bpy.utils.register_class(RenderNodeStringOperate)


def unregister():
    bpy.utils.unregister_class(RenderNodeStringOperate)
