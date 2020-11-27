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

    def process(self):
        dict = {}
        dict["Engine"] = 'BLENDER_EEVEE'
        for input in self.inputs:
            try:
                if input.is_linked:
                    dict[input.name] = input.links[0].from_socket[input.name]
                else:
                    try:
                        dict[input.name] = input.default_value
                    except:
                        pass
            except Exception as e:
                print(f"Render Settings {e}")
        self.outputs["Render Settings"]["Render Settings"] = dict

def register():
    bpy.utils.register_class(RSNodeEeveeRenderSettingsNode)