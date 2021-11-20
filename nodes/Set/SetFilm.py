import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetFilm(RenderNodeBase):
    bl_idname = 'RenderNodeSetFilm'
    bl_label = 'Set Film'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketString', 'engine', 'Render Engine')
        self.create_input('RenderNodeSocketBool', 'film_transparent', 'Transparent')
        # eevee
        i = self.create_input('RenderNodeSocketFloat', 'filter_size', 'Filter Size', default_value=1.5)
        i.hide = True
        i = self.create_input('RenderNodeSocketBool', 'use_overscan', 'Overscan')
        i.hide = True
        i = self.create_input('RenderNodeSocketFloat', 'overscan_size', 'Overscan Size', default_value=2)
        i.hide = True

        # cylces
        i = self.create_input('RenderNodeSocketFloat', 'film_exposure', 'Exposure')
        i.hide = True
        i = self.create_input('RenderNodeSocketFloat', 'filter_width', 'Filter Width', default_value=1.5)
        i.hide = True
        i = self.create_input('RenderNodeSocketBool', 'film_transparent_glass', 'Transparent Glass')
        i.hide = True
        i = self.create_input('RenderNodeSocketFloat', 'film_transparent_roughness', 'Transparent Roughness Threshold',
                              default_value=0.1)
        i.hide = True

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        if not self.process_task(): return

        engine = self.inputs['engine']
        if engine is None or engine == '': return

        film_transparent = self.inputs['film_transparent'].get_value()

        self.show_input('filter_size', engine == 'BLENDER_EEVEE')
        self.show_input('use_overscan', engine == 'BLENDER_EEVEE')
        self.show_input('overscan_size', engine == 'BLENDER_EEVEE' and self.inputs['use_overscan'].get_value() is True)

        self.show_input('film_exposure', engine == 'CYCLES')
        self.show_input('filter_width', engine == 'CYCLES')
        self.show_input('film_transparent_glass', engine == 'CYCLES')
        self.show_input('film_transparent_roughness', engine == 'CYCLES')

        if film_transparent is not None:
            self.compare(context.scene.render, 'film_transparent', film_transparent)

        if engine == 'BLENDER_EEVEE':
            value = self.inputs['filter_size'].get_value()
            if value: self.compare(context.scene.render.eevee, 'filter_size', value)
            value = self.inputs['use_overscan'].get_value()
            if value: self.compare(context.scene.render.eevee, 'use_overscan', value)
            value = self.inputs['overscan_size'].get_value()
            if value: self.compare(context.scene.render.eevee, 'overscan_size', value)
        elif engine == 'CYCLES':
            value = self.inputs['film_exposure'].get_value()
            if value: self.compare(context.scene.render.cycles, 'film_exposure', value)
            value = self.inputs['filter_width'].get_value()
            if value: self.compare(context.scene.render.cycles, 'filter_width', value)
            value = self.inputs['film_transparent_glass'].get_value()
            if value: self.compare(context.scene.render.cycles, 'film_transparent_glass', value)
            value = self.inputs['film_transparent_roughness'].get_value()
            if value: self.compare(context.scene.render.cycles, 'film_transparent_roughness', value)


def register():
    bpy.utils.register_class(RenderNodeSetFilm)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetFilm)
