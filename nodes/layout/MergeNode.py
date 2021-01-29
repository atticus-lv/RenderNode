import bpy
from bpy.props import *
from ...node_tree import RenderStackNode


class RSNodeSettingsMergeNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeSettingsMergeNode'
    bl_label = 'Merge'

    node_type: EnumProperty(name='node type', items=[
        ('SWITCH', 'Switch', ''),
        ('MERGE', 'Merge', '')
    ], default='MERGE')

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        if self.node_type == 'MERGE':
            try:
                if hasattr(bpy.context.space_data, 'edit_tree'):
                    if bpy.context.space_data.edit_tree.nodes.active.name == self.name:
                        row = layout.row(align=1)
                        a = row.operator("rsnode.edit_input", icon='ADD', text='Add')
                        a.socket_type = 'RSNodeSocketTaskSettings'
                        a.socket_name = "Input"
                        r = row.operator("rsnode.edit_input", icon='REMOVE', text='Del')
                        r.remove = 1

            except Exception:
                pass
        else:
            layout.operator('rsn.switch_setting').node = self.name

def register():
    bpy.utils.register_class(RSNodeSettingsMergeNode)


def unregister():
    bpy.utils.unregister_class(RSNodeSettingsMergeNode)
