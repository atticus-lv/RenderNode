import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
import json


class RenderNodeGetObject(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetObject'
    bl_label = 'Get Object'

    def init(self, context):
        self.create_input('RenderNodeSocketString', 'name', 'Name')
        self.create_output('RenderNodeSocketObject', 'object', 'Object')

    def draw_buttons(self, context, layout):
        pass

    def process(self, context, id, path):
        obj = None
        name = self.inputs['name'].get_value()
        if name is not None:
            obj = bpy.data.objects.get(name)

        if obj is not None:
            self.outputs['object'].set_value(obj)


def register():
    bpy.utils.register_class(RenderNodeGetObject)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetObject)
