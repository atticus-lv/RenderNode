import bpy
from RenderStackNode.node_tree import RenderStackNode


class RSNodeOutputSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeOutputSettingsNode'
    bl_label = 'Output Settings'

    def init(self, context):
        self.inputs.new('NodeSocketInt', 'Frame Start')
        self.inputs.new('NodeSocketInt', 'Frame End')
        self.inputs.new('NodeSocketInt', 'Frame Step')
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

        self.inputs["Frame Step"].default_value = 1

    def draw_buttons(self, context, layout):
        pass



def register():
    bpy.utils.register_class(RSNodeOutputSettingsNode)

def unregister():
    bpy.utils.unregister_class(RSNodeOutputSettingsNode)