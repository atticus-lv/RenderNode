import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
import random


def update_node(self, context):
    self.remove_output('output')

    if self.operator_type == 'random':
        self.create_output('RenderNodeSocketFloat', 'output', 'Output')

    if self.operator_type == 'randint':
        self.create_input('RenderNodeSocketInt', 'a', 'Start', default_value=1)
        self.create_input('RenderNodeSocketInt', 'b', 'End', default_value=5)
        self.create_output('RenderNodeSocketInt', 'output', 'Output')
    else:
        self.remove_input('a')
        self.remove_input('b')

    if self.operator_type == 'choice':
        self.create_input('RenderNodeSocketString', 'str', 'String')
        self.create_output('RenderNodeSocketString', 'output', 'Output')

    else:
        self.remove_input('str')

    self.execute_tree()


class RenderNodeRandomInput(RenderNodeBase):
    bl_idname = 'RenderNodeRandomInput'
    bl_label = 'Random Input'

    operator_type: EnumProperty(items=[
        ('random', 'Float from 0 to 1', ''),
        ('randint', 'Int from range', ''),
        ('choice', 'Choose charater', ''),

    ], default='random', update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'seed', 'Seed', default_value=0)
        self.create_output('RenderNodeSocketInt', 'output', 'Output')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operator_type', text='')

    def process(self, context, id, path):
        seed = self.inputs['seed'].get_value()
        if seed is None: return
        random.seed(seed)

        if self.operator_type == 'randint':
            a = self.inputs['a'].get_value()
            b = self.inputs['b'].get_value()
            if a is not None and b is not None:
                self.outputs[0].set_value(random.randint(a, b))
        elif self.operator_type == 'random':
            self.outputs[0].set_value(random.random())
        elif self.operator_type == 'choice':
            s = self.inputs['str'].get_value()
            if s is not None and len(s) > 0:
                try:
                    self.outputs[0].set_value(random.choice(s))
                except IndexError:
                    pass

def register():
    bpy.utils.register_class(RenderNodeRandomInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeRandomInput)
