import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetSceneViewLayer(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneViewLayer'
    bl_label = 'Set Scene View Layer'

    view_layer_name: StringProperty(name="View Layer Name", default="")

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketViewLayer', "view_layer", 'ViewLayer')
        self.create_input('RenderNodeSocketBool', 'use_for_render', 'Use for Rendering', default_value=True)

    def draw_buttons(self, context, layout):
        if self.view_layer_name != '':
            create = layout.operator('rsn.create_compositor_node', text='Comp Passes Output', icon='ADD')
            create.view_layer = self.view_layer_name
            create.use_passes = True

            remove = layout.operator('rsn.create_compositor_node', text='Remove Passes Output', icon='REMOVE')
            remove.view_layer = self.view_layer_name
            remove.use_passes = False
        else:
            layout.label(text="No View Layer Selected")

    def process(self, context, id, path):
        if not self.process_task(): return

        view_layer_name = self.inputs['view_layer'].get_value()
        view_layer = context.scene.view_layers.get(view_layer_name)

        if view_layer:
            self.view_layer_name = view_layer_name  # store view layer name for later use
            # set context view layer
            self.compare(context.window, 'view_layer', view_layer)
            self.compare(view_layer, 'use', self.inputs['use_for_render'].get_value())
        else:
            self.view_layer_name = ""

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
