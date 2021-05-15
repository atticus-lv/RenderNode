import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


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


class RenderNodeObjectData(RenderStackNode):
    bl_idname = 'RenderNodeObjectData'
    bl_label = 'Object Data'

    d_type = None
    value = None

    float_value: FloatProperty(name='Value', update=update_node)
    string_value: StringProperty(name='Value', update=update_node)
    bool_value: BoolProperty(name='Check', update=update_node)
    int_value: IntProperty(name='Value', update=update_node)

    color_value: FloatVectorProperty(name='Color', update=update_node, subtype='COLOR',
                                     default=(1.0, 1.0, 1.0),
                                     min=0.0, max=1.0)
    vector_value: FloatVectorProperty(name='Vector', update=update_node)

    def init(self, context):
        self.create_prop('RenderNodeSocketObject', 'object', "Object")
        self.create_prop('RenderNodeSocketString', 'data_path', "Data Path")

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.width = 200

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        self.store_data()
        d_type = self.get_data_type()

        if d_type is None:
            pass
        elif d_type == int:
            layout.prop(self, 'int_value')
        elif d_type == float:
            layout.prop(self, 'float_value')
        elif d_type == str:
            layout.prop(self, 'string_value')
        elif d_type == bool:
            layout.prop(self, 'bool_value', toggle=1)
        elif d_type == Color:
            layout.prop(self, 'color_value')
        elif d_type == Vector:
            layout.prop(self, 'vector_value')

    def get_data_type(self):
        self.store_data()
        ob = self.node_dict['object']
        dp = self.node_dict['data_path']

        try:
            obj, data_path = source_attr(ob, dp)
            if hasattr(obj.data, data_path):
                d_type = type(getattr(obj.data, data_path, None))
                return d_type
        except Exception as e:
            return None

    def process(self):
        d_type = self.get_data_type()

        value = None

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

        self.store_data()
        self.node_dict['value'] = value

        ob = self.node_dict['object']
        if ob:
            try:
                value = self.node_dict['value']
                obj, attr = source_attr(ob.data, self.node_dict['data_path'])
                self.compare(obj, attr, value)
            except Exception as e:
                pass
                # self.set_warning(msg=f"{e}")


# def register():
#     bpy.utils.register_class(RenderNodeObjectData)
#
#
# def unregister():
#     bpy.utils.unregister_class(RenderNodeObjectData)
