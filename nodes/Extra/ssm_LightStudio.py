import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RSNodeLightStudioNode(RenderNodeBase):
    bl_idname = 'RSNodeLightStudioNode'
    bl_label = 'SSM Light Studio'

    light_studio_index: IntProperty(name='light studio index', update=update_node)

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

    def process(self, context, id, path):
        index = self.light_studio_index
        try:
            self.compare(bpy.context.scene.ssm, 'light_studio_index', index)
        except Exception as e:
            print(f'SSM LightStudio node error:{e}')


def register():
    bpy.utils.register_class(RSNodeLightStudioNode)


def unregister():
    bpy.utils.unregister_class(RSNodeLightStudioNode)
