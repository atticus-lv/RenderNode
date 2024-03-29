import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    ob = self.inputs['object'].get_value()
    if self.data_path == '' or not ob: return None
    try:

        full_data_path = f'bpy.data.objects["{ob.name}"].data.' + self.data_path

        self.d_type = type(eval(full_data_path))

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
            self.create_input('RenderNodeSocketVector', 'value', "Vector")

        self.execute_tree()

    except Exception as e:
        print(e)


def source_attr(src_obj, scr_data_path):
    def get_obj_and_attr(obj, data_path):
        path = data_path.split('.')
        if len(path) == 1:
            return obj, path[0]
        else:
            back_obj = getattr(obj, path[0])
            back_path = '.'.join(path[1:])
            return get_obj_and_attr(back_obj, back_path)

    return get_obj_and_attr(src_obj, scr_data_path)


class RenderNodeObjectData(RenderNodeBase):
    bl_idname = 'RenderNodeObjectData'
    bl_label = 'Object Data'

    data_path: StringProperty(name='Data Path',
                              description='Data Path (Object Data Tab)',
                              default='', update=update_node)
    full_data_path = None
    d_type = None

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', "Object")
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')

        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, 'data_path')
        if self.d_type not in {int, float, str, bool, Color, Vector, None}:
            layout.label(text='Only support int, float, str, bool, Color, Vector')

    def process(self,context,id,path):
        ob = self.inputs['object'].get_value()
        if ob:
            obj, attr = source_attr(ob.data, self.data_path)
            self.compare(obj, attr, self.inputs['value'].get_value())


def register():
    bpy.utils.register_class(RenderNodeObjectData)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectData)
