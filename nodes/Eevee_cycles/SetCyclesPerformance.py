import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

def update_node(self, context):
    self.execute_tree()


class RenderNodeSetCyclesPerformance(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetCyclesPerformance'
    bl_label = 'Set Cycles Performance'

    threads_mode: EnumProperty(items=[
        ('AUTO', 'Auto-Detect', ''),
        ('FIXED', 'Fixed', ''),
    ], default='AUTO',name = "Threads Mode",update=update_node)

    preview_pixel_size: EnumProperty(items=[
        ('AUTO', 'Automatic', ''),
        ('1', '1x', ''),
        ('2', '2x', ''),
        ('4', '4x', ''),
        ('8', '8x', ''),
    ], default='AUTO',name = "Pixel Size",update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')


        i = self.create_input('RenderNodeSocketInt', 'threads', 'Threads', default_value=1)
        i.hide = True

        self.create_input('RenderNodeSocketBool', 'use_auto_tile', 'Use Tiling',
                          default_value=True)
        self.create_input('RenderNodeSocketInt', 'tile_size', 'Tile Size', default_value=2048)

        self.create_input('RenderNodeSocketBool', 'use_persistent_data', 'Persistent Data', default_value=False)


    def draw_buttons(self, context, layout):
        layout.prop(self, 'threads_mode')

    def process(self, context, id, path):
        if not self.process_task(): return

        value = self.inputs['use_auto_tile'].get_value()
        self.inputs['tile_size'].hide = False if value is True else True

        value = self.threads_mode
        self.inputs['threads'].hide = False if value == 'AUTO' else True

        for input in self.inputs:
            key = input.name
            value = input.get_value()

            if key in {'use_auto_tile','tile_size'}:
                self.compare(context.scene.cycles, key, value)
            else:
                self.compare(context.scene.render, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetCyclesPerformance)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCyclesPerformance)
