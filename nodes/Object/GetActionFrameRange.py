import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeGetActionFrameRange(RenderNodeBase):
    bl_idname = 'RenderNodeGetActionFrameRange'
    bl_label = 'Get Action Frame Range'

    def init(self, context):
        self.create_input('RenderNodeSocketAction', 'action', 'Action')
        self.create_output('RenderNodeSocketInt', 'frame_start', 'Start')
        self.create_output('RenderNodeSocketInt', 'frame_end', 'End')

    def process(self, context, id, path):
        action = self.inputs['action'].get_value()

        if action:
            self.outputs['frame_start'].set_value(round(action.frame_range[0]))
            self.outputs['frame_end'].set_value(round(action.frame_range[1]))


def register():
    bpy.utils.register_class(RenderNodeGetActionFrameRange)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetActionFrameRange)
