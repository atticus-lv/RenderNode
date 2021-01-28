import bpy
from bpy.props import *
from ...node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeLightStudioNode(RenderStackNode):
    bl_idname = 'RSNodeLightStudioNode'
    bl_label = 'SSM Light Studio'

    light_studio_index: IntProperty(name='light studio index',update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def get_name(self):
        if hasattr(bpy.context.scene, "ssm"):
            if len(bpy.context.scene.ssm.light_studio) > 0:
                if self.light_studio_index + 1 > len(bpy.context.scene.ssm.light_studio):
                    return None
                else:
                    return bpy.context.scene.ssm.light_studio[self.light_studio_index].name

    def draw_buttons(self, context, layout):
        name = self.get_name()
        if name:
            layout.label(text=name)
        else:
            layout.label(text='No such light studio')

        layout.prop(self, "light_studio_index", text='Index')


def register():
    bpy.utils.register_class(RSNodeLightStudioNode)


def unregister():
    bpy.utils.unregister_class(RSNodeLightStudioNode)
