import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


class RenderNodeSceneViewLayer(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneViewLayer'
    bl_label = 'Scene View Layer (experiment)'

    def init(self, context):
        self.create_prop('RenderNodeSocketViewLayer', "view_layer", 'ViewLayer')
        self.create_prop('RenderNodeSocketBool', 'use', 'Use for Rendering')
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def process(self):
        self.store_data()
        view_layer_name = self.node_dict['view_layer']
        view_layer = bpy.context.scene.view_layers.get(view_layer_name)

        if view_layer != '':
            self.compare(bpy.context.window, 'view_layer', view_layer)
            self.compare(view_layer, 'use', self.node_dict['use'])


# [
#     attr
#     for attr in dir(C.view_layer)
#     if attr.startswith("use_pass") and getattr(C.view_layer, attr) == True
# ]

def register():
    bpy.utils.register_class(RenderNodeSceneViewLayer)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneViewLayer)
