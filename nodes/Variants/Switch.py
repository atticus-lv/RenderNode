import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_socket(self, context):
    socket_type = 'RenderNodeSocket' + self.operate_type
    inputs = [input for input in self.inputs if input.name != 'active']
    inputs = list(reversed(inputs))
    if self.count > len(inputs):
        for i in range(self.count - len(inputs)):
            self.inputs.new(socket_type, 'Value')
    elif self.count < len(inputs):
        for i in range(len(inputs) - self.count):
            self.inputs.remove(inputs[i])


def update_node(self, context):
    socket_type = 'RenderNodeSocket' + self.operate_type
    for i, input in enumerate(self.inputs):
        if i == 0: continue
        self.inputs.remove(input)

    _connect = self.outputs['output'].connected_socket

    self.remove_output('output')
    output = self.create_output(socket_type, 'output', 'Output')
    if _connect:
        self.id_data.links.new(_connect, output)

    update_socket(self,context)

    self.execute_tree()


class RenderNodeSwitch(RenderNodeBase):
    bl_idname = 'RenderNodeSwitch'
    bl_label = 'Switch'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('', 'Base Type', ''),
            ('Int', 'Int', ''),
            ('Float', 'Float', ''),
            ('Bool', 'Boolean', ''),
            None,
            ('String', 'String', ''),
            ('ViewLayer', 'ViewLayer', ''),
            ('FilePath', 'FilePath', ''),

            None,
            ('XYZ', 'Vector', ''),
            ('Translation', 'Translation', ''),
            ('Euler', 'Rotation', ''),

            ('', 'Pointer', ''),
            ('Object', 'Object', ''),
            ('Material', 'Material', ''),
            ('World', 'World', ''),
            ('Collection', 'Collection', ''),
            ('Text', 'Text', ''),
        ],
        update=update_node, default='Float'
    )

    count: IntProperty(name='Count', default=2, update=update_socket, min=2)

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'active', "Active Input")
        self.create_input('RenderNodeSocketFloat', 'value1', "Value")
        self.create_input('RenderNodeSocketFloat', 'value2', "Value")
        self.create_output('RenderNodeSocketFloat', 'output', "Output")

        self.width = 175

    def draw_buttons(self, context, layout):
        row = layout.split(factor=0.5, align=1)
        row.prop(self, 'count')
        row.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        active = self.inputs['active'].get_value()
        if not active: return

        for i, input in enumerate(self.inputs):
            if i != active: continue
            ans = input.get_value()
            self.outputs[0].set_value(ans)


def register():
    bpy.utils.register_class(RenderNodeSwitch)


def unregister():
    bpy.utils.unregister_class(RenderNodeSwitch)
