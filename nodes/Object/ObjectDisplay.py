import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeObjectDisplay(RenderNodeBase):
    bl_idname = 'RenderNodeObjectDisplay'
    bl_label = 'Object Display'

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_input('RenderNodeSocketBool', 'hide_viewport', 'Hide Viewport')
        self.create_input('RenderNodeSocketBool', 'hide_render', 'Hide Render')

        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')

        self.width = 175

    def process(self,context,id,path):
        ob = self.inputs['object'].get_value()
        hide_viewport = self.inputs['hide_viewport'].get_value()
        hide_render = self.inputs['hide_render'].get_value()
        if ob:
            self.compare(ob, 'hide_viewport', hide_viewport)
            self.compare(ob, 'hide_render', hide_render)


def register():
    bpy.utils.register_class(RenderNodeObjectDisplay)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectDisplay)
