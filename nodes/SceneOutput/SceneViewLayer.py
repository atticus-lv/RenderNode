import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSceneViewLayer(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneViewLayer'
    bl_label = 'Scene View Layer'

    def init(self, context):
        self.create_input('RenderNodeSocketViewLayer', "view_layer", 'ViewLayer')
        self.create_input('RenderNodeSocketBool', 'set_as_active_layer', 'Set as active Layer')
        self.create_input('RenderNodeSocketBool', 'use_for_render', 'Use for Rendering')
        self.create_input('RenderNodeSocketBool','output_composite_passes','Output Composite Passes')
        self.create_output('RSNodeSocketTaskSettings','Settings','Settings')

    def process(self,context,id,path):
        view_layer_name = self.inputs['view_layer'].get_value()
        view_layer = bpy.context.scene.view_layers.get(view_layer_name)

        if view_layer:
            if self.inputs['set_as_active_layer'].get_value():
                self.compare(bpy.context.window, 'view_layer', view_layer)
            self.compare(view_layer, 'use', self.inputs['use_for_render'].get_value())

            # create comp node tree
            try:
                bpy.ops.rsn.create_compositor_node(
                    view_layer=view_layer_name,
                    use_passes=self.inputs['output_composite_passes'].get_value())
            except Exception as e:
                print(f'View Layer Passes {self.name} error:{e}')

# [
#     attr
#     for attr in dir(C.view_layer)
#     if attr.startswith("use_pass") and getattr(C.view_layer, attr) == True
# ]

def register():
    bpy.utils.register_class(RenderNodeSceneViewLayer)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneViewLayer)
