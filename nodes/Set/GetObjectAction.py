import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetObjectAction(RenderNodeBase):
    bl_idname = 'RenderNodeGetObjectAction'
    bl_label = 'Get Object Animation Action'

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object', show_text=False)
        self.create_output('RenderNodeSocketAction', 'action', 'Action')

    def process(self, context, id, path):
        ob = self.inputs['object'].get_value()

        if ob:
            self.outputs['action'].set_value(ob.animation_data.action)


def register():
    bpy.utils.register_class(RenderNodeGetObjectAction)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetObjectAction)
