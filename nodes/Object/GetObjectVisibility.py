import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetObjectVisibility(RenderNodeBase):
    bl_idname = 'RenderNodeGetObjectVisibility'
    bl_label = 'Get Object Visibility'

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object', show_text=False)
        self.create_output('RenderNodeSocketBool', 'hide_viewport', 'Show In Viewports',
                           default_value=True)  # invert bool
        self.create_output('RenderNodeSocketBool', 'hide_render', 'Show In Render', default_value=True)  # invert bool

    def process(self, context, id, path):
        ob = self.inputs['object'].get_value()

        if ob:
            self.outputs['hide_viewport'].set_value(not ob.hide_viewport)
            self.outputs['hide_render'].set_value(not ob.hide_render)



def register():
    bpy.utils.register_class(RenderNodeGetObjectVisibility)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetObjectVisibility)
