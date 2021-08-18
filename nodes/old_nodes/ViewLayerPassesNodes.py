import bpy
from bpy.props import *

from nodes.BASE.node_base import RenderNodeBase
from preferences import get_pref


def update_node(self, context):
    self.execute_tree()


class RSNodeViewLayerPassesNode(RenderNodeBase):
    bl_idname = "RSNodeViewLayerPassesNode"
    bl_label = "View Layer Passes"

    use_passes: BoolProperty(name="Separate Passes", update=update_node)
    view_layer: StringProperty(name="View Layer", default="", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "view_layer", context.scene, "view_layers", icon="RENDERLAYERS", text='')
        layout.prop(self, 'use_passes', toggle=1)

    def process(self, context, id, path):
        try:
            bpy.ops.rsn.create_compositor_node(
                view_layer=self.view_layer,
                use_passes=self.use_passes)
        except Exception as e:
            print(f'View Layer Passes {self.name} error:{e}')


def register():
    bpy.utils.register_class(RSNodeViewLayerPassesNode)


def unregister():
    bpy.utils.unregister_class(RSNodeViewLayerPassesNode)
