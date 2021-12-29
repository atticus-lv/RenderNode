import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
import json


def update_node(self, context):
    if self.operator_type == 'NAME':
        self.create_input('RenderNodeSocketString', 'name', 'Name')
    else:
        self.remove_input('name')

    if self.operator_type == 'OBJECT':
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_input('RenderNodeSocketInt', 'index', 'Index', default_value=0)
    else:
        self.remove_input('object')
        self.remove_input('index')

    if self.operator_type == 'INDEX':
        self.create_input('RenderNodeSocketInt', 'index', 'Index', default_value=0)
    else:
        self.remove_input('index')

    self.execute_tree()


class RenderNodeGetMaterial(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetMaterial'
    bl_label = 'Get Material'

    operator_type: EnumProperty(items=[
        ('NAME', 'Name',''),
        ('INDEX', 'Library Index',''),
        ('OBJECT', 'Object Slot',''),
    ], default='NAME', update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketString', 'name', 'Name')
        self.create_output('RenderNodeSocketMaterial', 'material', 'Material')

    def draw_buttons(self, context, layout):
        layout.prop(self,'operator_type',text='')

    def process(self, context, id, path):
        mat = None
        if self.operator_type == 'NAME':
            name = self.inputs['name'].get_value()
            if name is not None: mat = bpy.data.materials.get(name)

        elif self.operator_type == 'INDEX':
            index = self.inputs['index'].get_value()
            if index is not None and len(bpy.data.materials) > index:
                mat = bpy.data.materials[index]

        elif self.operator_type == 'OBJECT':
            index = self.inputs['index'].get_value()
            object = self.inputs['object'].get_value()

            if index is not None and object:
                if index < object.material_slots:
                    mat = object.material_slots[index]

        if mat is not None:
            self.outputs['material'].set_value(mat)


def register():
    bpy.utils.register_class(RenderNodeGetMaterial)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetMaterial)
