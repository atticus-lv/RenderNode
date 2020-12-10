import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

def update_passes_output(self,context):
    if self.use_passes:
        bpy.ops.rsn.creat_compositor_node(view_layer = self.view_layer)
    else:
        bpy.ops.rsn.creat_compositor_node(remove = 1)

class RSNodePassesNode(RenderStackNode):
    bl_idname = "RSNodePassesNode"
    bl_label = "Passes"

    use_passes:BoolProperty(update=update_passes_output,name = "Separate Passes")
    view_layer: StringProperty(update=update_passes_output,default="")

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "view_layer", context.scene, "view_layers", icon="RENDERLAYERS", text="")
        layout.prop(self,'use_passes')

def register():
    bpy.utils.register_class(RSNodePassesNode)

def unregister():
    bpy.utils.unregister_class(RSNodePassesNode)