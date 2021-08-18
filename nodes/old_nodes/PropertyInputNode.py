import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class RSNodePropertyInputNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodePropertyInputNode'
    bl_label = 'Property'

    full_data_path: StringProperty(name='Full Data Path', default='', update=update_node)

    float_value: FloatProperty(name='Value', update=update_node)
    string_value: StringProperty(name='Value', update=update_node)
    bool_value: BoolProperty(name='Check', update=update_node)
    int_value: IntProperty(name='Value', update=update_node)

    color_value: FloatVectorProperty(name='Color', update=update_node, subtype='COLOR',
                                     default=(1.0, 1.0, 1.0),
                                     min=0.0, max=1.0)
    vector_value: FloatVectorProperty(name='Vector', update=update_node)

    object_value: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 250

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, 'full_data_path')
        if self.full_data_path != '':
            try:
                d_type = type(eval(self.full_data_path))
                self.draw_custom_value(d_type, layout)
            except Exception:
                pass

    def draw_custom_value(self, d_type, layout):
        if d_type == int:
            layout.prop(self, 'int_value')
        elif d_type == Color:
            layout.prop(self, 'color_value')
        elif d_type == Vector:
            layout.prop(self, 'vector_value')
        elif d_type == float:
            layout.prop(self, 'float_value')
        elif d_type == str:
            layout.prop(self, 'string_value')
        elif d_type == bool:
            layout.prop(self, 'bool_value', toggle=1)
        elif d_type == bpy.types.Object:
            layout.prop(self, 'object_value')
        else:
            layout.label('Path Error')

    def get_data(self):
        task_data_obj = {}
        value = None
        if self.full_data_path != '':
            try:
                d_type = type(eval(self.full_data_path))
                if d_type == int:
                    value = self.int_value
                elif d_type == float:
                    value = self.float_value
                elif d_type == str:
                    value = self.string_value
                elif d_type == bool:
                    value = self.bool_value
                elif d_type == Color:
                    value = list(self.color_value)
                elif d_type == Vector:
                    value = list(self.vector_value)

                if value != None:
                    task_data_obj[self.name] = {
                        'full_data_path': self.full_data_path,
                        'value'         : value}

            except KeyError:
                self.set_warning()
        print(task_data_obj)
        return task_data_obj


def register():
    bpy.utils.register_class(RSNodePropertyInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodePropertyInputNode)
