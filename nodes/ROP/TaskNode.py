import bpy
from RenderStackNode.node_tree import RenderStackNode


class RSNodeTaskNode(RenderStackNode):
    '''A simple Task node'''
    bl_idname = 'RSNodeTaskNode'
    bl_label = 'Task'

    def init(self, context):
        self.inputs.new('RSNodeSocketCameraSettings', "Camera Settings")
        self.inputs.new('RSNodeSocketRenderSettings', "Render Settings", )
        self.inputs.new('RSNodeSocketOutputSettings', "Output Settings")

        self.outputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'name')

    def process(self):
        dict = {}
        dict["name"] = self.name

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
                print(f"Task {e}")

        self.outputs["Task"]["Task"] = dict


def register():
    bpy.utils.register_class(RSNodeTaskNode)
