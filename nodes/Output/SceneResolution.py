import os
import re

import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def get_preset_folder():
    bl_path = os.getcwd()
    version = f'{bpy.app.version[0]}' + '.' + f'{bpy.app.version[1]}'
    return os.path.join(bl_path, version, 'scripts', 'presets')


def get_all_preset_path():
    folder = os.path.join(get_preset_folder(), 'render')
    return [os.path.join(folder, filename) for filename in os.listdir(folder) if filename.endswith('.py')]


def get_preset_data(path):
    with open(path, 'r') as f:
        data = f.read()
        res_x = re.search(r"resolution_x = (\d.*)\s", data).group(1)
        res_y = re.search(r"resolution_y = (\d.*)\s", data).group(1)
        res_scale = re.search('resolution_percentage = (\d.*)\s', data).group(1)
        return int(res_x), int(res_y), int(res_scale)


def read_and_get_preset():
    """
    :parm:preset{name:[x,y,percentage]}
    """
    preset = {}

    paths = get_all_preset_path()
    for path in paths:
        preset[os.path.basename(path)[:-3]] = get_preset_data(path)

    return preset


preset = read_and_get_preset()


class RSN_OT_SetSceneResolutionNodePreset(bpy.types.Operator):
    bl_idname = 'rsn.set_scene_resolution_node_preset'
    bl_label = 'Set node resolution'

    res_x: IntProperty()
    res_y: IntProperty()
    res_scale: IntProperty()

    def execute(self, context):
        node = bpy.context.space_data.edit_tree.nodes.active
        if not node:
            return {"FINISHED"}

        node.inputs['resolution_x'].value = self.res_x
        node.inputs['resolution_y'].value = self.res_y
        node.inputs['resolution_percentage'].value = self.res_scale

        return {"FINISHED"}


class RSN_MT_NodeResolutionPresetsMenu(bpy.types.Menu):
    bl_label = "Resolution Preset"
    bl_idname = "RSN_MT_NodeResolutionPresetsMenu"

    def draw(self, context):
        layout = self.layout
        for key, value in preset.items():
            op = layout.operator('rsn.set_scene_resolution_node_preset', text=key)
            op.res_x = value[0]
            op.res_y = value[1]
            op.res_scale = value[2]


class RenderNodeSceneResolution(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneResolution'
    bl_label = 'Scene Resolution'

    def init(self, context):
        self.create_input('RenderNodeSocketInt', "resolution_x", 'X', default_value=1920)
        self.create_input('RenderNodeSocketInt', "resolution_y", 'Y', default_value=1080)
        self.create_input('RenderNodeSocketInt', "resolution_percentage", '%', default_value=100)

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        try:
            if bpy.context.space_data.node_tree.nodes.active.name == self.name:
                layout.menu('RSN_MT_NodeResolutionPresetsMenu')
            else:
                layout.label(text='Active Presets', icon='RESTRICT_SELECT_OFF')
        except Exception:
            pass

    def process(self):
        # correct number
        if self.inputs['resolution_x'].get_value() < 4:
            self.inputs['resolution_x'].set_value(4)
        if self.inputs['resolution_y'].get_value() < 4:
            self.inputs['resolution_y'].set_value(4)
        if self.inputs['resolution_percentage'].get_value() < 1:
            self.inputs['resolution_percentage'].set_value(1)

        bpy.context.scene.render.resolution_x = self.inputs['resolution_x'].get_value()
        bpy.context.scene.render.resolution_y = self.inputs['resolution_y'].get_value()
        bpy.context.scene.render.resolution_percentage = self.inputs['resolution_percentage'].get_value()


def register():
    bpy.utils.register_class(RenderNodeSceneResolution)
    bpy.utils.register_class(RSN_OT_SetSceneResolutionNodePreset)
    bpy.utils.register_class(RSN_MT_NodeResolutionPresetsMenu)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneResolution)
    bpy.utils.unregister_class(RSN_OT_SetSceneResolutionNodePreset)
    bpy.utils.unregister_class(RSN_MT_NodeResolutionPresetsMenu)
