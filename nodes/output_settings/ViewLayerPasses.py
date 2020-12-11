import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeViewLayerPassesNode(RenderStackNode):
    bl_idname = "RSNodeViewLayerPassesNode"
    bl_label = "View Layer Passes"

    use_passes: BoolProperty(name="Separate Passes")
    view_layer: StringProperty(name="View Layer", default="")

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "view_layer", context.scene, "view_layers", icon="RENDERLAYERS", text='')
        layout.prop(self, 'use_passes', toggle=1)


def register():
    bpy.utils.register_class(RSNodeViewLayerPassesNode)


def unregister():
    bpy.utils.unregister_class(RSNodeViewLayerPassesNode)
