import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


class RenderNodeObjectDisplay(RenderStackNode):
    bl_idname = 'RenderNodeObjectDisplay'
    bl_label = 'Object Display +'

    def init(self, context):
        self.create_prop('RenderNodeSocketObject', 'object', 'Object')
        self.create_prop('RenderNodeSocketBool', 'hide_viewport', 'Hide Viewport')
        self.create_prop('RenderNodeSocketBool', 'hide_render', 'Hide Render')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.width = 175

    def process(self):
        self.store_data()

        ob = self.node_dict['object']
        if ob:
            self.compare(ob, 'hide_viewport', self.node_dict['hide_viewport'])
            self.compare(ob, 'hide_render', self.node_dict['hide_render'])


def register():
    bpy.utils.register_class(RenderNodeObjectDisplay)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectDisplay)
