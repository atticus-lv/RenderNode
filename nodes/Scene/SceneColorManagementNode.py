import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

import os
import re


def get_ocio_path():
    """get current blender version cm"""
    bl_path = os.getcwd()
    version = f'{bpy.app.version[0]}' + '.' + f'{bpy.app.version[1]}'
    cs_folder = os.path.join(bl_path, version, 'datafiles', 'colormanagement')

    return os.path.join(cs_folder, 'config.ocio')


def search_ocio(rule: str):
    """use re to find certain words"""
    ocio_path = get_ocio_path()
    with open(ocio_path, mode='r') as f:
        config = f.read()
        list = re.findall(rule, config)

    return list


# re rules
rule_display_device = r"active_displays: \[(.*?)]"
rule_view_transform = r"active_views: \[(.*?)]"
rule_look = r"- !<Look>\s.*name:\s(.*)\s"

# list to enum_property
list_display_device = [name for name in search_ocio(rule_display_device)[0].split(', ')]
enum_display_device = [(name, name, '') for name in list_display_device]

list_view_transform = [name for name in search_ocio(rule_view_transform)[0].split(', ')]
enum_view_transform = [(name, name, '') for name in list_view_transform]

list_look = [name for name in search_ocio(rule_look)]
list_look.append('None')
enum_look = [(name, name, '') for name in list_look]


def update_node(self, context):
    self.update_parms()


class RSNodeColorManagementNode(RenderNodeBase):
    '''A simple input node'''
    bl_idname = 'RenderNodeSceneColorManagement'
    bl_label = 'Scene Color Management'

    # display_device: EnumProperty(name='Display Device', update=update_node,
    #                              items=enum_display_device)

    view_transform: EnumProperty(name='View Transform', update=update_node,
                                 items=enum_view_transform)

    look: EnumProperty(name='Look', update=update_node,
                       items=enum_look)

    ev: FloatProperty(name="Exposure Value", default=0, soft_min=-3, soft_max=3, update=update_node)
    gamma: FloatProperty(name="Gamma", default=1.0, update=update_node)

    def init(self, context):
        self.creat_input('RenderNodeSocketFloat', 'exposure', 'Exposure', default_value=0.0)
        self.creat_input('RenderNodeSocketFloat', 'gamma', 'Gamma', default_value=1.0)

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.width = 200

        # init value
        self.view_transform = bpy.context.scene.view_settings.view_transform
        self.look = bpy.context.scene.view_settings.look

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)

        # col.prop(self, 'display_device')
        col.prop(self, 'view_transform')
        col.prop(self, 'look')

    def process(self):
        vs = bpy.context.scene.view_settings

        self.compare(vs, 'exposure', self.inputs['exposure'].get_value())
        self.compare(vs, 'gamma', self.inputs['gamma'].get_value())

        self.compare(vs, 'view_transform', self.view_transform)
        self.compare(vs, 'look', self.look)


def register():
    bpy.utils.register_class(RSNodeColorManagementNode)


def unregister():
    bpy.utils.unregister_class(RSNodeColorManagementNode)
