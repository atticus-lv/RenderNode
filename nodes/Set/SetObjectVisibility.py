import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetObjectVisibility(RenderNodeBase):
    bl_idname = 'RenderNodeSetObjectVisibility'
    bl_label = 'Set Object Visibility'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_input('RenderNodeSocketObject', 'object', '')
        self.create_input('RenderNodeSocketBool', 'hide_viewport', 'Show In Viewports',default_value = True) # invert bool
        self.create_input('RenderNodeSocketBool', 'hide_render', 'Show In Render',default_value = True) # invert bool

        self.create_output('RenderNodeSocketTask', 'task', 'Task')


    def process(self,context,id,path):
        self.process_task()
        ob = self.inputs['object'].get_value()
        hide_viewport = self.inputs['hide_viewport'].get_value()
        hide_render = self.inputs['hide_render'].get_value()
        if ob:
            self.compare(ob, 'hide_viewport', not hide_viewport)
            self.compare(ob, 'hide_render', not hide_render)


def register():
    bpy.utils.register_class(RenderNodeSetObjectVisibility)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetObjectVisibility)
