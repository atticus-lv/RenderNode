import bpy
from bpy.props import *

from ...nodes.BASE.node_tree import RenderStackNode
from ...preferences import get_pref


def update_node(self, context):
    self.update_parms()


class RenderNodeSceneFrameRange(RenderStackNode):
    bl_idname = "RenderNodeSceneFrameRange"
    bl_label = "Scene Frame Range"

    def init(self, context):
        self.create_prop('RenderNodeSocketInt', 'frame_start', 'Start')
        self.create_prop('RenderNodeSocketInt', 'frame_end', 'End')
        self.create_prop('RenderNodeSocketInt', 'frame_step', 'Step')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.inputs['frame_start'].value = bpy.context.scene.frame_start
        self.inputs['frame_end'].value = bpy.context.scene.frame_end
        self.inputs['frame_step'].value = bpy.context.scene.frame_step

    def process(self):
        # correct input
        if self.inputs['frame_start'].value > self.inputs['frame_end'].value:
            self.inputs['frame_end'].value = self.inputs['frame_start'].value
        if self.inputs['frame_step'].value < 1: self.inputs['frame_step'].value = 1

        self.store_data()

        self.compare(bpy.context.scene, 'frame_start', self.node_dict['frame_start'])
        self.compare(bpy.context.scene, 'frame_end', self.node_dict['frame_end'])
        self.compare(bpy.context.scene, 'frame_step', self.node_dict['frame_step'])

        task_node = bpy.context.space_data.node_tree.nodes.get(bpy.context.window_manager.rsn_viewer_node)
        if task_node:
            task_node.frame_start = self.node_dict['frame_start']
            task_node.frame_end = self.node_dict['frame_end']
            task_node.frame_step = self.node_dict['frame_step']

def register():
    bpy.utils.register_class(RenderNodeSceneFrameRange)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneFrameRange)
