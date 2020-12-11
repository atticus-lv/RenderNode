import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

class RSNodeViewLayerInputNode(RenderStackNode):
    bl_idname = 'RSNodeViewLayerInputNode'
    bl_label = 'View Layer'

    view_layer: StringProperty(name="View Layer",
                               description='Just Check Out View Layer, you should set its details in property panel')

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        # self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "view_layer", context.scene, "view_layers", icon="RENDERLAYERS",text='')

    def draw_buttons_ext(self, context, layout):
        layout.label(text="Just Check Out View Layer")
        layout.label(text="You should set its details in property panel")


def register():
    bpy.utils.register_class(RSNodeViewLayerInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeViewLayerInputNode)
