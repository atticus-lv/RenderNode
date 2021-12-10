import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetSceneViewLayer(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneViewLayer'
    bl_label = 'Set Scene View Layer'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketViewLayer', "view_layer", 'ViewLayer')
        self.create_input('RenderNodeSocketBool', 'use_for_render', 'Use for Rendering', default_value=True)
        self.create_input('RenderNodeSocketBool', 'output_composite_passes', 'Output Composite Passes')

    def process(self, context, id, path):
        if not self.process_task(): return

        view_layer_name = self.inputs['view_layer'].get_value()
        view_layer = context.scene.view_layers.get(view_layer_name)

        if view_layer:
            self.compare(context.window, 'view_layer', view_layer)
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

# [
#     attr
#     for attr in dir(C.view_layer)
#     if getattr(C.view_layer, attr) == True
# ]


def register():
    bpy.utils.register_class(RenderNodeSetSceneViewLayer)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetSceneViewLayer)
