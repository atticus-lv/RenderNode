import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetSceneFrame(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetSceneFrame'
    bl_label = 'Get Scene Frame'


    def init(self, context):
        self.create_output('RenderNodeSocketInt', "frame_current", 'Frame')

    def process(self,context,id,path):
        self.outputs[0].set_value(context.scene.frame_current)



def register():
    bpy.utils.register_class(RenderNodeGetSceneFrame)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetSceneFrame)
