import bpy
from bpy.props import *

from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RenderNodeSetWorkBenchSamples(RenderNodeBase):
    bl_idname = "RenderNodeSetWorkBenchSamples"
    bl_label = "Set WorkBench Samples"

    render_aa: EnumProperty(name='Render',
                            items=[('OFF', 'No Anti-Aliasing', ''), ('FXAA', 'Single Pass Anti-Aliasing', ''),
                                   ('5', '5 Samples', ''), ('8', '8 Samples', ''),
                                   ('11', '11 Samples', ''), ('16', '16 Samples', ''),
                                   ('32', '32 Samples', '')],
                            default='8',
                            update=update_node)

    viewport_aa: EnumProperty(name='Viewport',
                              items=[('OFF', 'No Anti-Aliasing', ''), ('FXAA', 'Single Pass Anti-Aliasing', ''),
                                     ('5', '5 Samples', ''), ('8', '8 Samples', ''),
                                     ('11', '11 Samples', ''), ('16', '16 Samples', ''),
                                     ('32', '32 Samples', '')],
                              default='FXAA',
                              update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'render_aa')
        layout.prop(self, 'viewport_aa')

    def process(self, context, id, path):
        if not self.process_task(): return

        try:
            self.compare(context.scene.display, 'render_aa', self.render_aa)
            self.compare(context.scene.display, 'viewport_aa', self.viewport_aa)
        except Exception as e:
            print(e)


def register():
    bpy.utils.register_class(RenderNodeSetWorkBenchSamples)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetWorkBenchSamples)
