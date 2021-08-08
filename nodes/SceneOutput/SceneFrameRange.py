import bpy
from bpy.props import *

from ...nodes.BASE.node_base import RenderNodeBase
from ...preferences import get_pref


def update_node(self, context):
    self.execute_tree()


class RenderNodeSceneFrameRange(RenderNodeBase):
    bl_idname = "RenderNodeSceneFrameRange"
    bl_label = "Scene Frame Range"

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'frame_start', 'Start')
        self.create_input('RenderNodeSocketInt', 'frame_end', 'End')
        self.create_input('RenderNodeSocketInt', 'frame_step', 'Step')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.inputs['frame_start'].default_value = bpy.context.scene.frame_start
        self.inputs['frame_end'].default_value = bpy.context.scene.frame_end
        self.inputs['frame_step'].default_value = 1

    def process(self,context,id,path):
        # correct input
        start = self.inputs['frame_start'].get_value()
        end = self.inputs['frame_end'].get_value()
        if start > end:
            self.inputs['frame_end'].set_value(start)

        if self.inputs['frame_step'].get_value() < 1: self.inputs['frame_step'].set_value(1)

        frame_start = self.inputs['frame_start'].get_value()
        frame_end = self.inputs['frame_end'].get_value()
        frame_step = self.inputs['frame_step'].get_value()

        task_node = bpy.context.space_data.node_tree.nodes.get(bpy.context.window_manager.rsn_viewer_node)
        if task_node:
            task_node.frame_start = frame_start
            task_node.frame_end = frame_end
            task_node.frame_step = frame_step


def register():
    bpy.utils.register_class(RenderNodeSceneFrameRange)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneFrameRange)
