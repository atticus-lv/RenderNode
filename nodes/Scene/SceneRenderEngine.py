import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode

from collections import defaultdict


def update_node(self, context):
    if self.engine in {'CYCLES', 'BLENDER_EEVEE'}:
        self.create_prop('RenderNodeSocketInt', 'samples', 'Render', default_value=64)
        self.create_prop('RenderNodeSocketInt', 'viewport_samples', 'Viewport', default_value=64)

    else:
        self.remove_prop('samples')
        self.remove_prop('viewport_samples')

    self.update_parms()


class RenderNodeSceneRenderEngine(RenderStackNode):
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
        self.create_prop('RenderNodeSocketInt', 'samples', 'Samples', default_value=64)
        self.create_prop('RenderNodeSocketInt', 'viewport_samples', 'Viewport', default_value=64)

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

    def process(self):
        self.store_data()

        if self.engine == 'CYCLES':
            self.compare(bpy.context.scene.cycles, 'samples', self.node_dict['samples'])
            self.compare(bpy.context.scene.cycles, 'preview_samples', self.node_dict['viewport_samples'])
            self.compare(bpy.context.scene.cycles, 'device', self.cycles_device)
        elif self.engine == 'BLENDER_EEVEE':
            self.compare(bpy.context.scene.eevee, 'taa_render_samples', self.node_dict['samples'])
            self.compare(bpy.context.scene.eevee, 'taa_samples', self.node_dict['viewport_samples'])

        elif self.engine == 'BLENDER_WORKBENCH':
            self.compare(bpy.context.scene.display, 'render_aa', self.render_aa)
            self.compare(bpy.context.scene.display.shading, 'light', self.light)
            self.compare(bpy.context.scene.display.shading, 'studio_light', self.studio_light)

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
