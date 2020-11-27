import bpy
from RenderStackNode.node_tree import RenderStackNode

class RSNodeEeveeRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeEeveeRenderSettingsNode'
    bl_label = 'Eevee Settings'



    def init(self, context):
        self.inputs.new('NodeSocketInt', "Samples")
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

        self.inputs["Samples"].default_value = 128

    def draw_buttons(self, context, layout):
        pass



def register():
    bpy.utils.register_class(RSNodeEeveeRenderSettingsNode)

def unregister():
    bpy.utils.unregister_class(RSNodeEeveeRenderSettingsNode)