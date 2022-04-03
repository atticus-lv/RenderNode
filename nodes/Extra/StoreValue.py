import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from mathutils import Color, Vector


def update_node(self, context):
    # remove
    socket_type = 'RenderNodeSocket' + self.operate_type
    for i, input in enumerate(self.inputs):
        self.inputs.remove(input)

    self.remove_output('output')
    output = self.create_output(socket_type, 'output', 'Output')
    self.create_input(socket_type, 'value', 'Input Value')
    self.create_input(socket_type, 'store_value', 'Store Value')

    try:
        _connect = self.outputs['output'].connected_socket

        if _connect:
            self.id_data.links.new(_connect, output)
    except:
        pass

    self.execute_tree()


class RenderNodeStoreValue(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeStoreValue'
    bl_label = 'Store Value'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('Int', 'Int', ''),
            ('Float', 'Float', ''),
            ('Bool', 'Boolean', ''),
            ('String', 'String', ''),
            ('XYZ', 'Vector', ''),
        ],
        update=update_node, default='Float'
    )

    store: BoolProperty(name='Is Storing Value', default=False)

    def init(self, context):
        self.create_output('RenderNodeSocketFloat', 'output', 'Value')
        self.create_input('RenderNodeSocketFloat', 'value', 'Input Value')
        self.create_input('RenderNodeSocketFloat', 'store_value', 'Store Value')
        # self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type')
        layout.prop(self, 'store')

    def process(self, context, id, path):
        try:
            value_input = self.inputs['value'].get_value()

            if self.store is False:
                self.inputs['store_value'].default_value = value_input
                self.outputs['output'].set_value(value_input)
                self.store = True
            else:
                store_value = self.inputs['store_value'].get_value()
                self.outputs['output'].set_value(store_value)


        except Exception as e:
            print(e)


def register():
    bpy.utils.register_class(RenderNodeStoreValue)


def unregister():
    bpy.utils.unregister_class(RenderNodeStoreValue)
