import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    socket_type = 'RenderNodeSocket' + self.operate_type
    self.remove_input('value1')
    self.remove_input('value2')
    self.create_input(socket_type, 'value1', 'True')
    self.create_input(socket_type, 'value2', 'False')

    self.execute_tree()


class RenderNodeSwitch(RenderNodeBase):
    bl_idname = 'RenderNodeSwitch'
    bl_label = 'Switch'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('Float', 'Float', ''),
            ('String', 'String', ''),
            ('Int', 'Int', ''),
            ('Bool', 'Boolean', ''),
            ('XYZ', 'Vector', ''),
        ],
        update=update_node, default='Float'
    )

    def init(self, context):
        self.create_input('RenderNodeSocketBool', 'switch', 'True/False')
        self.create_input('RenderNodeSocketFloat', 'value1', 'True')
        self.create_input('RenderNodeSocketFloat', 'value2', 'False')
        self.create_output('RenderNodeSocketFloat', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type')

    def process(self, context, id, path):
        switch = self.inputs['switch'].get_value()
        t = self.inputs['value1'].get_value()
        f = self.inputs['value2'].get_value()
        ans = t if switch is True else f
        self.outputs[0].set_value(ans)


def register():
    bpy.utils.register_class(RenderNodeSwitch)


def unregister():
    bpy.utils.unregister_class(RenderNodeSwitch)
