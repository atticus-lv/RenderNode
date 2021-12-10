import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetSceneViewLayer(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetSceneViewLayer'
    bl_label = 'Get Scene View Layer'

    def init(self, context):
        self.create_output('RenderNodeSocketViewLayer', "view_layer", 'ViewLayer')


    def process(self, context, id, path):
        self.outputs['view_layer'].set_value(context.window.view_layer.name)


def register():
    bpy.utils.register_class(RenderNodeGetSceneViewLayer)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetSceneViewLayer)
