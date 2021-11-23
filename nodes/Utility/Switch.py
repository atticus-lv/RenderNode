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
            self.inputs.new(socket_type, self.operate_type)
    elif self.count < len(inputs):
        for i in range(len(inputs) - self.count):
            self.inputs.remove(inputs[i])


def update_node(self, context):
    # remove
    socket_type = 'RenderNodeSocket' + self.operate_type
    for i, input in enumerate(self.inputs):
        if i == 0: continue
        self.inputs.remove(input)

    self.remove_output('output')
    output = self.create_output(socket_type, 'output', 'Output')
    # add socket
    update_socket(self, context)

    try:
        _connect = self.outputs['output'].connected_socket

        if _connect:
            self.id_data.links.new(_connect, output)
    except:
        pass

    self.execute_tree()


from ..BASE._runtime import cache_node_dependants


class RenderNodeSwitch(RenderNodeBase):
    bl_idname = 'RenderNodeSwitch'
    bl_label = 'Switch'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('', 'Base Type', ''),
            ('Task', 'Task', ''),
            None,
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
            ('Action', 'Action', ''),
            ('World', 'World', ''),
            ('Collection', 'Collection', ''),
            ('Text', 'Text', ''),
        ],
        update=update_node, default='Task'
    )

    count: IntProperty(name='Count', default=2, update=update_socket, min=2)

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'active', "Active Input")
        self.operate_type = 'Task'

        self.width = 175

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')
        layout.prop(self, 'count')

    def execute_dependants(self, context, id, path):
        # first execute the not set task type
        nodes, indexs = self.get_dependant_nodes()

        if 0 in indexs:
            self.execute_other(context, id, path, nodes[0])
        active = self.inputs['active'].get_value()

        for i, node in enumerate(nodes):
            index = indexs[i]
            if active is not None and index == active:
                self.execute_other(context, id, path, node)

    def process(self, context, id, path):
        active = self.inputs['active'].get_value()
        if active is None: return

        for i, input in enumerate(self.inputs):
            if i != 0 and i == active:
                ans = input.get_value()

                self.outputs[0].set_value(ans)
                break

def register():
    bpy.utils.register_class(RenderNodeSwitch)


def unregister():
    bpy.utils.unregister_class(RenderNodeSwitch)
