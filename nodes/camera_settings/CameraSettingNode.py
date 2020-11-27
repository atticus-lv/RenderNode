import bpy
from RenderStackNode.node_tree import RenderStackNode


class RSNodeCameraSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCameraSettingsNode'
    bl_label = 'Camera Settings'

    def init(self, context):
        self.inputs.new('RSNodeSocketCamera', "Camera")
        self.inputs.new('NodeSocketInt', "Res X", )
        self.inputs.new('NodeSocketInt', "Res Y")
        self.inputs.new('NodeSocketInt', "Res Scale")

        self.outputs.new('RSNodeSocketCameraSettings', "Camera Settings")

        self.inputs["Res X"].default_value = 1920
        self.inputs["Res Y"].default_value = 1080
        self.inputs["Res Scale"].default_value = 100

    def draw_buttons(self, context, layout):
        pass




def register():
    bpy.utils.register_class(RSNodeCameraSettingsNode)

def unregister():
    bpy.utils.unregister_class(RSNodeCameraSettingsNode)