import bpy
from bpy.props import *
from ...node_tree import RenderStackNode


class RSNodeSettingsMergeNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeSettingsMergeNode'
    bl_label = 'Merge Settings'

    node_type: EnumProperty(name='node type', items=[
        ('OUTPUT_SETTINGS', 'Output Settings', ''),
        ('RENDER_SETTINGS', 'Render Settings', ''),
        ('SETTINGS', 'Settings', '')
    ], default='OUTPUT_SETTINGS')

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 180

    def draw_buttons(self, context, layout):
        try:
            if hasattr(bpy.context.space_data, 'edit_tree'):
                if bpy.context.space_data.edit_tree.nodes.active.name == self.name:
                    row = layout.row(align=1)
                    a = row.operator("rsnode.edit_input", icon='ADD', text='Add')
                    a.socket_type = 'RSNodeSocketTaskSettings'
                    a.socket_name = "Settings"
                    r = row.operator("rsnode.edit_input", icon='REMOVE', text='Del')
                    r.remove = 1

        except Exception:
            pass


def register():
    bpy.utils.register_class(RSNodeSettingsMergeNode)


def unregister():
    bpy.utils.unregister_class(RSNodeSettingsMergeNode)
