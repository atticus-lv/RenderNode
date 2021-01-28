import bpy
from bpy.props import *
from ...node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeViewLayerPassesNode(RenderStackNode):
    bl_idname = "RSNodeViewLayerPassesNode"
    bl_label = "View Layer Passes"

    use_passes: BoolProperty(name="Separate Passes", update=update_node)
    view_layer: StringProperty(name="View Layer", default="", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "view_layer", context.scene, "view_layers", icon="RENDERLAYERS", text='')
        layout.prop(self, 'use_passes', toggle=1)


def register():
    bpy.utils.register_class(RSNodeViewLayerPassesNode)


def unregister():
    bpy.utils.unregister_class(RSNodeViewLayerPassesNode)
