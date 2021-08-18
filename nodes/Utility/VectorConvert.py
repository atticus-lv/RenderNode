import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type == 'COMBINE':
        self.remove_output('x')
        self.remove_output('y')
        self.remove_output('z')
        self.remove_input('input')
        self.create_input('RenderNodeSocketFloat', 'x', 'X')
        self.create_input('RenderNodeSocketFloat', 'y', 'Y')
        self.create_input('RenderNodeSocketFloat', 'z', 'Z')
        self.create_output('RenderNodeSocketXYZ', 'output', "Output")

    else:
        self.remove_input('x')
        self.remove_input('y')
        self.remove_input('z')
        self.remove_output('output')
        self.create_input('RenderNodeSocketXYZ', 'input', 'Input')
        self.create_output('RenderNodeSocketFloat', 'x', 'X')
        self.create_output('RenderNodeSocketFloat', 'y', 'Y')
        self.create_output('RenderNodeSocketFloat', 'z', 'Z')

    self.execute_tree()


class RenderNodeVectorConvert(RenderNodeBase):
    bl_idname = 'RenderNodeVectorConvert'
    bl_label = 'Vector Convert'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('COMBINE', 'Combine', ''),
            ('SEPARATE', 'Separate', ''),
        ],
        update=update_node
    )

    def init(self, context):
        self.create_input('RenderNodeSocketFloat', 'x', 'X')
        self.create_input('RenderNodeSocketFloat', 'y', 'Y')
        self.create_input('RenderNodeSocketFloat', 'z', 'Z')
        self.create_output('RenderNodeSocketXYZ', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type')

    def process(self,context,id,path):
        if self.operate_type == 'COMBINE':
            res = Vector((
                self.inputs[0].get_value(),
                self.inputs[1].get_value(),
                self.inputs[2].get_value(),
            ))
            self.outputs[0].set_value(res)
        else:
            input_value = list(self.inputs[0].get_value())
            self.outputs[0].set_value(input_value[0])
            self.outputs[1].set_value(input_value[1])
            self.outputs[2].set_value(input_value[2])


def register():
    bpy.utils.register_class(RenderNodeVectorConvert)


def unregister():
    bpy.utils.unregister_class(RenderNodeVectorConvert)
