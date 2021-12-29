import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
import json


class RenderNodeGetCameraInfo(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeGetCameraInfo'
    bl_label = 'Get Camera Info'

    def init(self, context):
        self.create_output('RenderNodeSocketInt', 'lens', 'Focal Length')
        self.create_output('RenderNodeSocketFloat', 'shift_x', 'Shift X')
        self.create_output('RenderNodeSocketFloat', 'shift_y', 'Shift Y')
        self.create_output('RenderNodeSocketFloat', 'clip_start', 'Clip Start')
        self.create_output('RenderNodeSocketFloat', 'clip_end', 'Clip End')

        self.create_output('RenderNodeSocketFloat', 'focus_distance', 'Focus Distance')
        self.create_output('RenderNodeSocketFloat', 'aperture_fstop', 'F-Stop')

    def process(self, context, id, path):
        if not context.scene.camera: return

        attrs = ['lens', 'shift_x', 'shift_y', 'clip_start', 'clip_end']
        cam = context.scene.camera.data

        if cam:
            for attr in attrs:
                value = getattr(cam, attr)
                self.outputs[attr].set_value(value)

            self.outputs['focus_distance'].set_value(cam.dof.focus_distance)
            self.outputs['aperture_fstop'].set_value(cam.dof.aperture_fstop)


def register():
    bpy.utils.register_class(RenderNodeGetCameraInfo)


def unregister():
    bpy.utils.unregister_class(RenderNodeGetCameraInfo)
