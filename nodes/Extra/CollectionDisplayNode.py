import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RSNodeCollectionDisplayNode(RenderNodeBase):
    bl_idname = 'RSNodeCollectionDisplayNode'
    bl_label = 'Collection Display'

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.create_input('RenderNodeSocketCollection', 'collection', '')
        self.create_input('RenderNodeSocketBool', 'hide_viewport', 'Hide Viewport')
        self.create_input('RenderNodeSocketBool', 'hide_render', 'Hide Render')

    def process(self):
        coll = self.inputs['collection'].get_value()
        if coll:
            coll.hide_viewport = self.inputs['hide_viewport'].get_value()
            coll.hide_render = self.inputs['hide_render'].get_value()


def register():
    bpy.utils.register_class(RSNodeCollectionDisplayNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCollectionDisplayNode)
