import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    if self.operator_type == 'NAME':
        self.create_input('RenderNodeSocketString', 'name', 'Name')
    else:
        self.remove_input('name')

    if self.operator_type == 'INDEX':
        self.create_input('RenderNodeSocketInt', 'index', 'Index', default_value=0)
    else:
        self.remove_input('index')

    if self.operator_type == 'OBJECT':
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
    else:
        self.remove_input('object')

    self.execute_tree()


class RenderNodeGetAction(RenderNodeBase):
    bl_idname = 'RenderNodeGetAction'
    bl_label = 'Get Action'

    operator_type: EnumProperty(items=[
        ('NAME', 'Name', ''),
        ('INDEX', 'Library Index', ''),
        ('OBJECT', 'Object', ''),
    ], default='NAME', update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object', show_text=False)
        self.create_output('RenderNodeSocketAction', 'action', 'Action')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operator_type', text='')

    def process(self, context, id, path):
        act = None
        if self.operator_type == 'NAME':
            name = self.inputs['name'].get_value()
            if name is not None: act = bpy.data.actions.get(name)

        elif self.operator_type == 'INDEX':
            index = self.inputs['index'].get_value()
            if index is not None and len(bpy.data.actions) > index:
                act = bpy.data.actions[index]

        elif self.operator_type == 'OBJECT':
            object = self.inputs['object'].get_value()

            if object:
                act = object.animation_data.action

        if act is not None:
            self.outputs['action'].set_value(act)


def register():
    bpy.utils.register_class(RenderNodeGetAction)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetAction)
