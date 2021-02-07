import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RSNodeObjectDataNode(RenderStackNode):
    bl_idname = 'RSNodeObjectDataNode'
    bl_label = 'Object Data'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)

    data_path: StringProperty(name='Data Path', default='')

    float_value: FloatProperty(name='Value', update=update_node)
    string_value: StringProperty(name='Value', update=update_node)
    bool_value: BoolProperty(name='On', update=update_node)
    int_value: FloatProperty(name='Value', update=update_node)

    color_value: FloatVectorProperty(name='Color', update=update_node, subtype='COLOR',
                                     default=(1.0, 1.0, 1.0),
                                     min=0.0, max=1.0)
    vector_value: FloatVectorProperty(name='Vector', update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 250

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0

        row = layout.row(align=1)
        row.prop(self, 'object')
        layout.prop(self, 'data_path')

        if self.object:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.object.name
            if self.data_path != '' and hasattr(self.object.data, self.data_path):
                d_type = type(getattr(self.object.data, self.data_path, None))
                if d_type == int:
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


def register():
    bpy.utils.register_class(RSNodeObjectDataNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectDataNode)
