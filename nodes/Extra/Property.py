import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


def update_node(self, context):
    if self.full_data_path == '': return None

    try:
        self.d_type = type(eval(self.full_data_path))

        self.remove_prop('value')

        if self.d_type == int:
            self.create_prop('RenderNodeSocketInt', 'value', "Int")
        elif self.d_type == float:
            self.create_prop('RenderNodeSocketFloat', 'value', "Float")
        elif self.d_type == str:
            self.create_prop('RenderNodeSocketString', 'value', "String")
        elif self.d_type == bool:
            self.create_prop('RenderNodeSocketBool', 'value', "Bool")
        elif self.d_type == Color:
            self.create_prop('RenderNodeSocketColor', 'value', "Color")
        elif self.d_type == Vector:
            self.create_prop('RenderNodeSocketVector', 'value', "Vector")

        self.update_parms()

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
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, 'full_data_path')
        if self.d_type not in {int, float, str, bool, Color, Vector, None}:
            layout.label(text='Only support int, float, str, bool, Color, Vector')

    def process(self):
        self.store_data()
        if 'value' not in self.node_dict: return None

        try:
            obj = eval(self.full_data_path)
            if obj == self.node_dict['value']: return None

            exec(f'{self.full_data_path} = {self.node_dict["value"]}')

        except Exception as e:
            print(e)


def register():
    bpy.utils.register_class(RenderNodeProperty)


def unregister():
    bpy.utils.unregister_class(RenderNodeProperty)
