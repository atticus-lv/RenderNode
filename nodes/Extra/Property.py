import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


def update_node(self, context):
    if self.full_data_path == '': return None

    try:
        self.d_type = type(eval(self.full_data_path))

        self.remove_input('value')

        if self.d_type == int:
            self.create_input('RenderNodeSocketInt', 'value', "Int")
        elif self.d_type == float:
            self.create_input('RenderNodeSocketFloat', 'value', "Float")
        elif self.d_type == str:
            self.create_input('RenderNodeSocketString', 'value', "String")
        elif self.d_type == bool:
            self.create_input('RenderNodeSocketBool', 'value', "Boolean")
        elif self.d_type == Color:
            self.create_input('RenderNodeSocketColor', 'value', "Color")
        elif self.d_type == Vector:
            self.create_input('RenderNodeSocketXYZ', 'value', "Vector")

        self.execute_tree()

    except Exception as e:
        print(e)


class RenderNodeProperty(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeProperty'
    bl_label = 'Property'

    full_data_path: StringProperty(name='Path',
                                   description='Full Data Path',
                                   default='', update=update_node)

    d_type = None

    def init(self, context):
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, 'full_data_path')
        if self.d_type not in {int, float, str, bool, Color, Vector, None}:
            layout.label(text='Only support int, float, str, bool, Color, Vector')

    def process(self, context, id, path):
        try:
            obj = eval(self.full_data_path)
            if obj == self.inputs['value'].get_value(): return None

            value = self.inputs["value"].get_value()
            if type(value) in {Color,Vector}:value = list(value)
            exec(f'{self.full_data_path} = {value}')

        except Exception as e:
            print(e)


def register():
    bpy.utils.register_class(RenderNodeProperty)


def unregister():
    bpy.utils.unregister_class(RenderNodeProperty)
