import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetCollectionVisibility(RenderNodeBase):
    bl_idname = 'RenderNodeGetCollectionVisibility'
    bl_label = 'Get Collection Visibility'

    def init(self, context):
        self.create_input('RenderNodeSocketCollection', 'collection', 'Collection',show_text=False)
        self.create_output('RenderNodeSocketBool', 'hide_viewport', 'Show In Viewports',default_value = True) # invert bool
        self.create_output('RenderNodeSocketBool', 'hide_render', 'Show In Render',default_value = True) # invert bool



    def process(self,context,id,path):
        if not self.process_task():return
        coll = self.inputs['collection'].get_value()
        if coll:
            self.outputs['hide_viewport'].set_value(not coll.hide_viewport)
            self.outputs['hide_render'].set_value(not coll.hide_render)


def register():
    bpy.utils.register_class(RenderNodeGetCollectionVisibility)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetCollectionVisibility)
