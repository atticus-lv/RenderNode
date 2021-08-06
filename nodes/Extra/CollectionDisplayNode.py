import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RSNodeCollectionDisplayNode(RenderNodeBase):
    bl_idname = 'RSNodeCollectionDisplayNode'
    bl_label = 'Collection Display'

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.creat_input('RenderNodeSocketCollection', 'collection', '')
        self.creat_input('RenderNodeSocketBool', 'hide_viewport', 'Hide Viewport')
        self.creat_input('RenderNodeSocketBool', 'hide_render', 'Hide Render')

    def draw_buttons(self, context, layout):
        pass

    def process(self):
        self.store_data()

        coll = self.node_dict['collection']
        if coll:
            coll.hide_viewport = self.node_dict['hide_viewport']
            coll.hide_render = self.node_dict['hide_render']


def register():
    bpy.utils.register_class(RSNodeCollectionDisplayNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCollectionDisplayNode)
