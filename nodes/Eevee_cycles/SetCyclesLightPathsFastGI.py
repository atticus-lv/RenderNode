import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RenderNodeSetCyclesLightPathsFastGI(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesLightPathsFastGI'
    bl_label = 'Set Cycles Light Paths FastGI'

    fast_gi_method: EnumProperty(name = 'Method',items=[
        ('REPLACE', 'Replace', ''),
        ('ADD', 'Add', ''),
    ], default='REPLACE', update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'use_fast_gi', 'Enable', default_value=False)
        self.create_input('RenderNodeSocketFloat', 'ao_factor', 'AO Factor', default_value=1.0)
        self.create_input('RenderNodeSocketFloat', 'distance', 'AO Distance', default_value=10)
        self.create_input('RenderNodeSocketInt', 'ao_bounces', 'Viewport Bounces', default_value=1)
        self.create_input('RenderNodeSocketInt', 'ao_bounces_render', 'Render Bounces', default_value=1)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 175

    def draw_buttons(self, context, layout):
        layout.prop(self,'fast_gi_method')

    def process(self, context, id, path):
        if not self.process_task(): return

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            if key not in {'distance', 'ao_factor'}:
                self.compare(context.scene.cycles, key, value)
            else:
                self.compare(context.scene.world.light_settings, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesLightPathsFastGI)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesLightPathsFastGI)
