import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

from collections import defaultdict


def update_node(self, context):
    if self.engine == 'CYCLES':
        self.create_input('RenderNodeSocketInt', 'cycles_samples', 'Render', default_value=64)
        self.create_input('RenderNodeSocketInt', 'preview_samples', 'Viewport', default_value=64)
        self.create_input('RenderNodeSocketBool', 'use_adaptive_sampling', 'Adaptive Sampling', default_value=False)
    else:
        self.remove_input('cycles_samples')
        self.remove_input('preview_samples')
        self.remove_input('use_adaptive_sampling')

    if self.engine == 'BLENDER_EEVEE':
        self.create_input('RenderNodeSocketInt', 'taa_render_samples', 'Render', default_value=64)
        self.create_input('RenderNodeSocketInt', 'taa_samples', 'Viewport', default_value=64)
    else:
        self.remove_input('taa_render_samples')
        self.remove_input('taa_samples')

    if self.engine == 'LUXCORE':
        self.create_input('RenderStackNodeBool', 'use_samples', 'Use Samples', default=True)
        self.create_input('RenderNodeSocketInt', 'luxcore_samples', 'Half Samples', default_value=64)
        self.create_input('RenderStackNodeBool', 'use_time', 'Use Time', default=True)
        self.create_input('RenderNodeSocketInt', 'luxcore_time', 'Half Time', default_value=64)
    else:
        self.remove_input('use_samples')
        self.remove_input('luxcore_samples')
        self.remove_input('use_time')
        self.remove_input('luxcore_time')

    if self.engine == 'octane':
        self.create_input('RenderNodeSocketInt', 'max_samples', 'Max. samples', default_value=500)
        self.create_input('RenderNodeSocketInt', 'max_diffuse_depth', 'Max. diffuse depth', default_value=5)
        self.create_input('RenderNodeSocketInt', 'max_glossy_depth', 'Max. glossy depth', default_value=12)
        self.create_input('RenderNodeSocketInt', 'max_scatter_depth', 'Max. scatter depth', default_value=8)
    else:
        self.remove_input('max_samples')
        self.remove_input('max_diffuse_depth')
        self.remove_input('max_glossy_depth')
        self.remove_input('max_scatter_depth')

    self.execute_tree()


class RenderNodeSceneRenderEngine(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneRenderEngine'
    bl_label = 'Scene Render Engine'

    _enum_item_hack = []

    # cycles
    cycles_device: EnumProperty(name='Device',
                                items=[('CPU', 'CPU', ''),
                                       ('GPU', 'GPU', ''), ],
                                default='GPU',
                                update=update_node)
    # workbench
    light: EnumProperty(name='Lighting',
                        items=[('STUDIO', 'STUDIO', ''), ('MATCAP', 'MATCAP', ''), ('FLAT', 'FLAT', '')],
                        default='STUDIO',
                        update=update_node)

    render_aa: EnumProperty(name='Samples',
                            items=[('OFF', 'No Anti-Aliasing', ''), ('FXAA', 'Single Pass Anti-Aliasing', ''),
                                   ('5', '5 Samples', ''), ('8', '8 Samples', ''),
                                   ('11', '11 Samples', ''), ('16', '16 Samples', ''),
                                   ('32', '32 Samples', '')],
                            default='8',
                            update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'taa_render_samples', 'Render', default_value=64)
        self.create_input('RenderNodeSocketInt', 'taa_samples', 'Viewport', default_value=64)

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, "engine")

        if self.engine == 'CYCLES':
            col.prop(self, 'cycles_device')
        elif self.engine == 'BLENDER_WORKBENCH':
            col.prop(self, 'render_aa')
            col.prop(self, 'light')
            col.prop(self, 'studio_light')

    def process(self,context,id,path):
        # correct numbers
        for atrr in ['cycles_samples', 'preview_samples',
                     'taa_render_samples', 'taa_samples',
                     'luxcore_samples', 'luxcore_time',
                     'max_samples', 'max_diffuse_depth', 'max_glossy_depth', 'max_scatter_depth']:

            if atrr in self.inputs:
                if self.inputs[atrr].get_value() < 1: self.inputs[atrr].set_value(1)

        # engine
        if self.engine == 'CYCLES':
            self.compare(bpy.context.scene.cycles, 'samples', self.inputs['cycles_samples'].get_value())
            self.compare(bpy.context.scene.cycles, 'preview_samples', self.inputs['preview_samples'].get_value())
            self.compare(bpy.context.scene.cycles, 'use_adaptive_sampling', self.inputs['use_adaptive_sampling'].get_value())
            self.compare(bpy.context.scene.cycles, 'device', self.cycles_device)

        elif self.engine == 'BLENDER_EEVEE':
            self.compare(bpy.context.scene.eevee, 'taa_render_samples', self.inputs['taa_render_samples'].get_value())
            self.compare(bpy.context.scene.eevee, 'taa_samples', self.inputs['taa_samples'].get_value())

        elif self.engine == 'BLENDER_WORKBENCH':
            self.compare(bpy.context.scene.display, 'render_aa', self.render_aa)
            self.compare(bpy.context.scene.display.shading, 'light', self.light)
            self.compare(bpy.context.scene.display.shading, 'studio_light', self.studio_light)

        elif self.engine == 'LUXCORE':
            self.compare(bpy.context.scene.luxcore.halt, 'use_samples', self.inputs['use_samples'].get_value())
            self.compare(bpy.context.scene.luxcore.halt, 'use_time', self.inputs['use_time'].get_value())
            self.compare(bpy.context.scene.luxcore.halt, 'samples', self.inputs['luxcore_samples'].get_value())
            self.compare(bpy.context.scene.luxcore.halt, 'time', self.inputs['luxcore_time'].get_value())

        elif self.engine == 'octane':
            self.compare(bpy.context.scene.octane, 'max_samples', self.inputs['max_samples'].get_value())
            self.compare(bpy.context.scene.octane, 'max_diffuse_depth', self.inputs['max_diffuse_depth'].get_value())
            self.compare(bpy.context.scene.octane, 'max_glossy_depth', self.inputs['max_glossy_depth'].get_value())
            self.compare(bpy.context.scene.octane, 'max_scatter_depth', self.inputs['max_scatter_depth'].get_value())

        # switch engine
        self.compare(bpy.context.scene.render, 'engine', self.engine)

    def enum_studio_light(self, context):
        studio_lights = defaultdict(list)
        for sl in bpy.context.preferences.studio_lights:
            studio_lights[sl.type].append((sl.name, sl.name, ''))

        return studio_lights[self.light]

    def engine_enum_items(self, context):
        enum_items = RenderNodeSceneRenderEngine._enum_item_hack
        enum_items.clear()

        # append viewport engine
        enum_items.append(('BLENDER_EEVEE', 'Eevee', ''))
        enum_items.append(('BLENDER_WORKBENCH', 'Workbench', ''))

        addon = [engine.bl_idname for engine in bpy.types.RenderEngine.__subclasses__()]

        # append to enum_items
        for name in addon:
            enum_items.append((name, name.capitalize(), ''))

        return enum_items

    temp_engine = engine_enum_items
    engine: EnumProperty(name='Engine', description='Render Eninge available',
                         items=temp_engine,
                         update=update_node)

    temp_studio_light = enum_studio_light
    studio_light: EnumProperty(name='Studio Light', description='MATCAP available',
                               items=temp_studio_light,
                               update=update_node)


def register():
    bpy.utils.register_class(RenderNodeSceneRenderEngine)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneRenderEngine)
