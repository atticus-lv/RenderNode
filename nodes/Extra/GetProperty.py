import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


def update_node(self, context):
    if self.full_data_path == '': return None

    try:
        self.d_type = type(eval(self.full_data_path))

        self.remove_output('value')

        if self.d_type == int:
            self.create_output('RenderNodeSocketInt', 'value', "Int")
        elif self.d_type == float:
            self.create_output('RenderNodeSocketFloat', 'value', "Float")
        elif self.d_type == str:
            self.create_output('RenderNodeSocketString', 'value', "String")
        elif self.d_type == bool:
            self.create_output('RenderNodeSocketBool', 'value', "Boolean")
        elif self.d_type == Color:
            self.create_output('RenderNodeSocketColor', 'value', "Color")
        elif self.d_type == Vector:
            self.create_output('RenderNodeSocketXYZ', 'value', "Vector")

        self.execute_tree()

    except Exception as e:
        print(e)


class RenderNodeGetProperty(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetProperty'
    bl_label = 'Get Property'

    full_data_path: StringProperty(name='Path',
                                   description='Full Data Path',
                                   default='', update=update_node)

    d_type = None


    def init(self, context):
        self.create_output('RenderNodeSocketFloat', 'value', 'Value')
        # self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, 'full_data_path')
        if self.d_type not in {int, float, str, bool, Color, Vector, None}:
            layout.label(text='Only support int, float, str, bool, Color, Vector')

    def process(self, context, id, path):
        try:
            obj = eval(self.full_data_path)
            self.outputs['value'].set_value(obj)

        except Exception as e:
            print(e)


def register():
    bpy.utils.register_class(RenderNodeGetProperty)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetProperty)
