import os
import re

import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetSceneResolution(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneResolution'
    bl_label = 'Set Scene Resolution'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_input('RenderNodeSocketInt', "resolution_x", 'X', default_value=1920)
        self.create_input('RenderNodeSocketInt', "resolution_y", 'Y', default_value=1080)
        self.create_input('RenderNodeSocketInt', "resolution_percentage", '%', default_value=100)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def draw_buttons(self, context, layout):
        try:
            space = context.space_data
            path = space.path
            node = path[-1].node_tree.nodes.active

            if node and node == self:
                layout.menu('RSN_MT_NodeResolutionPresetsMenu')
            else:
                layout.label(text='Active Presets', icon='RESTRICT_SELECT_OFF')
        except Exception:
            pass

    def process(self, context, id, path):
        if not self.process_task():return

        # correct number
        if self.inputs['resolution_x'].get_value() < 4:
            self.inputs['resolution_x'].set_value(4)
        if self.inputs['resolution_y'].get_value() < 4:
            self.inputs['resolution_y'].set_value(4)
        if self.inputs['resolution_percentage'].get_value() < 1:
            self.inputs['resolution_percentage'].set_value(1)

        context.scene.render.resolution_x = self.inputs['resolution_x'].get_value()
        context.scene.render.resolution_y = self.inputs['resolution_y'].get_value()
        context.scene.render.resolution_percentage = self.inputs['resolution_percentage'].get_value()


def register():
    bpy.utils.register_class(RenderNodeSetSceneResolution)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetSceneResolution)
