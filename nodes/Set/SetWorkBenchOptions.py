import bpy
from bpy.props import *

from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RenderNodeSetWorkBenchOptions(RenderNodeBase):
    bl_idname = "RenderNodeSetWorkBenchOptions"
    bl_label = "Set WorkBench Options"

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
        self.create_input('RenderNodeSocketBool', 'show_backface_culling', 'Backface Culling')
        self.create_input('RenderNodeSocketBool', 'show_xray', 'Show X-Ray')
        i = self.create_input('RenderNodeSocketFloat', 'xray_alpha', 'X-Ray', default_value=0.5)
        i.hide = True
        self.create_input('RenderNodeSocketBool', 'show_shadows', 'Show Shadow')
        i = self.create_input('RenderNodeSocketFloat', 'shadow_intensity', 'Shadow', default_value=0.5)
        i.hide = True
        self.create_input('RenderNodeSocketBool', 'show_cavity', 'Cavity')
        self.create_input('RenderNodeSocketBool', 'use_dof', 'Depth of Field')
        self.create_input('RenderNodeSocketBool', 'show_object_outline', 'Outline')
        i = self.create_input('RenderNodeSocketColor', 'object_outline_color', 'Outline Color', default_value=(0.0, 0.0, 0.0))
        i.hide = True
        self.create_input('RenderNodeSocketBool', 'show_specular_highlight', 'Specular Lighting')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'render_aa')
        layout.prop(self, 'viewport_aa')

    def process(self, context, id, path):
        if not self.process_task(): return

        value = self.inputs['show_shadows'].get_value()
        self.inputs['shadow_intensity'].hide = False if value is True else True

        value = self.inputs['show_xray'].get_value()
        self.inputs['xray_alpha'].hide = False if value is True else True

        value = self.inputs['show_object_outline'].get_value()
        self.inputs['object_outline_color'].hide = False if value is True else True

        self.compare(context.scene.display, 'render_aa', self.render_aa)
        self.compare(context.scene.display, 'viewport_aa', self.viewport_aa)

        for input in self.inputs:
            if input.name == 'task': continue
            value = input.get_value()
            try:
                self.compare(context.scene.display.shading, input.name, value)
            except Exception as e:
                print(e)


def register():
    bpy.utils.register_class(RenderNodeSetWorkBenchOptions)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetWorkBenchOptions)
