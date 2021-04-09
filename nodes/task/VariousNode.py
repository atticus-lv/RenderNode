import bpy
from bpy.props import *
from ..BASE.node_tree import RenderStackNode


class RSNodeVariousNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeVariousNode'
    bl_label = 'Various'

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'name')

    def set_active(self, active):
        """:parm active: start from 1

        """
        if active > len(self.inputs):
            active = len(self.inputs)
        elif active < 1:
            active = 1

        for i, input in enumerate(self.inputs):
            if input.is_linked:
                node = input.links[0].from_node
                node.mute = 0 if active == i + 1 else 1

        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Input")

    def auto_update_inputs(self, socket_type, socket_name):
        super().auto_update_inputs(socket_type, socket_name)


def register():
    bpy.utils.register_class(RSNodeVariousNode)


def unregister():
    bpy.utils.unregister_class(RSNodeVariousNode)
