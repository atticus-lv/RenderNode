import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def update_node(self, context):
    self.update()


class RSNodeResolutionInputNode(RenderStackNode):
    bl_idname = "RSNodeResolutionInputNode"
    bl_label = "Resolution"

    res_x: IntProperty(name="Resolution X", default=1920, min=4, subtype='PIXEL', update=update_node)
    res_y: IntProperty(name="Resolution Y", default=1080, min=4, subtype='PIXEL', update=update_node)
    res_scale: IntProperty(name="Resolution Scale", default=100, min=1, subtype='PERCENTAGE', soft_min=1, soft_max=100,
                           update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        row = col.row(align=1)
        row.prop(self, 'res_x', text="X")
        row.prop(self, 'res_y', text="Y")
        col.prop(self, 'res_scale', text="%", slider=1)


def register():
    bpy.utils.register_class(RSNodeResolutionInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeResolutionInputNode)
