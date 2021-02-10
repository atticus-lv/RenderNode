import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import source_attr

import re
from mathutils import Color, Vector


def update_node(self, context):
    self.update_parms()


class RSNodeObjectModifierNode(RenderStackNode):
    bl_idname = 'RSNodeObjectModifierNode'
    bl_label = 'Object Modifier'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)

    data_path: StringProperty(name='Data Path', default='')

    float_value: FloatProperty(name='Value', update=update_node)
    string_value: StringProperty(name='Value', update=update_node)
    bool_value: BoolProperty(name='On', update=update_node)
    int_value: IntProperty(name='Value', update=update_node)

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
            if self.data_path != '':
                match = re.match(r"modifiers[[](.*?)[]]", self.data_path)
                name = match.group(1)
                if name:
                    data_path = self.data_path.split('.')[-1]
                    try:
                        modifier = self.object.modifiers[name[1:-1]]
                        try:
                            if isinstance(modifier, bpy.types.NodesModifier):
                                layout.label(text='Not support Geometry Node Modify yet')
                        except:
                            pass
                        if hasattr(modifier, data_path):
                            d_type = type(getattr(modifier, data_path, None))
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
                    except KeyError:
                        pass

    def get_data(self):
        task_data_obj = {}
        value = None
        if self.object and self.data_path != '':
            match = re.match(r"modifiers[[](.*?)[]]", self.data_path)
            name = match.group(1)
            if name:
                data_path = self.data_path.split('.')[-1]
                try:
                    modifier = self.object.modifiers[name[1:-1]]

                    if hasattr(modifier, data_path):
                        d_type = type(getattr(modifier, data_path, None))
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
                        task_data_obj[self.name] = {'object'   : self.object.name,
                                                    'data_path': self.data_path,
                                                    'value'    : value}
                except KeyError:
                    self.set_warning()

        return task_data_obj


def register():
    bpy.utils.register_class(RSNodeObjectModifierNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectModifierNode)
