import bpy
from bpy.props import *

from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RenderNodeSetWorkBenchColor(RenderNodeBase):
    bl_idname = "RenderNodeSetWorkBenchColor"
    bl_label = "Set WorkBench Color"

    color_type: EnumProperty(name='Color Type',
                             items=[
                                 ('MATERIAL', 'Material', ''),
                                 ('OBJECT', 'Object', ''),
                                 ('VERTEX', 'Vertex', ''),
                                 ('SINGLE', 'Single', ''),
                                 ('RANDOM', 'Random', ''),
                                 ('TEXTURE', 'Texture', ''),

                             ],
                             default='MATERIAL',
                             update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        i = self.create_input('RenderNodeSocketColor', 'single_color', 'Single Color')
        i.hide = True

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def draw_buttons(self, context, layout):
        layout.grid_flow(columns=3, align=True).prop(self, 'color_type', expand=True)

    def process(self, context, id, path):
        if not self.process_task(): return

        self.compare(context.scene.display.shading, 'color_type', self.color_type)

        self.inputs['single_color'].hide = False if self.color_type == 'SINGLE' else False
        value = self.inputs['single_color'].get_value()
        if value is not None:
            self.compare(context.scene.display.shading, 'single_color', value)


def register():
    bpy.utils.register_class(RenderNodeSetWorkBenchColor)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetWorkBenchColor)
