import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
import json


class RenderNodeGetObjectInfo(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetObjectInfo'
    bl_label = 'Get Object Info'

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_output('RenderNodeSocketTranslation', 'location', 'Location')
        self.create_output('RenderNodeSocketEuler', 'rotate', 'Rotation')
        self.create_output('RenderNodeSocketXYZ', 'scale', 'Scale')
        self.create_output('RenderNodeSocketString', 'name', 'Name')

    def process(self, context, id, path):
        ob = self.inputs['object'].get_value()
        if ob:
            self.outputs['location'].set_value(ob.location)
            self.outputs['rotate'].set_value(ob.rotation_euler)
            self.outputs['scale'].set_value(ob.scale)
            self.outputs['name'].set_value(ob.name)


def register():
    bpy.utils.register_class(RenderNodeGetObjectInfo)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetObjectInfo)
