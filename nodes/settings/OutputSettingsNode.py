import bpy
from RenderStackNode.node_tree import RenderStackNode


class RSNodeOutputSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeOutputSettingsNode'
    bl_label = 'Output Settings'

    def init(self, context):
        self.inputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        add = layout.operator("rsnode.edit_input", text="Add Output Settings")
        add.remove = False
        add.socket_type = "RSNodeSocketOutputSettings"
        add.socket_name  = "Output Settings"

        remove = layout.operator("rsnode.edit_input", text="Remove Unused")
        remove.remove = True


def register():
    bpy.utils.register_class(RSNodeOutputSettingsNode)

def unregister():
    bpy.utils.unregister_class(RSNodeOutputSettingsNode)