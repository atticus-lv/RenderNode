import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetCollectionVisibility(RenderNodeBase):
    bl_idname = 'RenderNodeSetCollectionVisibility'
    bl_label = 'Set Collection Visibility'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_input('RenderNodeSocketCollection', 'collection', '', show_text=False)
        self.create_input('RenderNodeSocketBool', 'hide_viewport', 'Show In Viewports',
                          default_value=True)  # invert bool
        self.create_input('RenderNodeSocketBool', 'hide_render', 'Show In Render', default_value=True)  # invert bool

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def process(self, context, id, path):
        if not self.process_task(): return
        coll = self.inputs['collection'].get_value()
        hide_viewport = self.inputs['hide_viewport'].get_value()
        hide_render = self.inputs['hide_render'].get_value()
        if hide_viewport is None or hide_render is None or coll is None: return
        # invert
        coll.hide_viewport = not hide_viewport
        coll.hide_render = not hide_render


def register():
    bpy.utils.register_class(RenderNodeSetCollectionVisibility)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetCollectionVisibility)
