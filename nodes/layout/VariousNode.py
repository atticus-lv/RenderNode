import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def active_various(self, context):
    if self.active > len(self.inputs):
        self.active = len(self.inputs)
    elif self.active < 1:
        self.active = 1

    for i, input in enumerate(self.inputs):
        if input.is_linked:
            node = input.links[0].from_node
            node.mute = 0 if self.active == i + 1 else 1

    dg = context.evaluated_depsgraph_get()
    dg.update()

    self.update_parms()


class RSNodeVariousNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeVariousNode'
    bl_label = 'Various'

    active: IntProperty(name='Active Var', default=1, update=active_various)

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self,'name')
        layout.prop(self,"active")
        # if len(self.inputs) >= self.active and self.inputs[self.active-1].is_linked:
        #     node = self.inputs[self.active-1].links[0].from_node
        #     layout.label(text=node.name)

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Input")

    def auto_update_inputs(self, socket_type, socket_name):
        super().auto_update_inputs(socket_type, socket_name)


def register():
    bpy.utils.register_class(RSNodeVariousNode)


def unregister():
    bpy.utils.unregister_class(RSNodeVariousNode)
