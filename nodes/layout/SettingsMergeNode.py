import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeSettingsMergeNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeSettingsMergeNode'
    bl_label = 'Merge Settings'

    node_type: EnumProperty(name='node type', items=[
        ('OUTPUT_SETTINGS', 'Output Settings', ''),
        ('RENDER_SETTINGS', 'Render Settings', ''),
        ('SETTINGS', 'Settings', '')
    ],
                            default='OUTPUT_SETTINGS'
                            )

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 180

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        if self.node_type == 'OUTPUT_SETTINGS':
            add = layout.operator("rsnode.edit_input", text="Add Output Settings",icon = 'ADD')
            add.remove = False
            add.socket_type = "RSNodeSocketOutputSettings"
            add.socket_name = "Output Settings"
        elif self.node_type == 'RENDER_SETTINGS':
            add = layout.operator("rsnode.edit_input", text="Add Render Settings",icon = 'ADD')
            add.remove = False
            add.socket_type = "RSNodeSocketRenderSettings"
            add.socket_name = "Render Settings"
        else:
            add = layout.operator("rsnode.edit_input", text="Add Settings", icon='ADD')
            add.remove = False
            add.socket_type = "RSNodeSocketTaskSettings"
            add.socket_name = "Settings"

        remove = layout.operator("rsnode.edit_input", text="Remove Unused",icon = 'REMOVE')
        remove.remove = True


def register():
    bpy.utils.register_class(RSNodeSettingsMergeNode)


def unregister():
    bpy.utils.unregister_class(RSNodeSettingsMergeNode)
