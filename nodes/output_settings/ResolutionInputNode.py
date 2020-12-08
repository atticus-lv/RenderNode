import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

class RSNodeResolutionInputNode(RenderStackNode):
    bl_idname = "RSNodeResolutionInputNode"
    bl_label = "Resolution"

    res_x:IntProperty(name = "Resolution X",default=1920,min = 4,subtype='PIXEL')
    res_y:IntProperty(name = "Resolution Y",default=1080,min = 4,subtype='PIXEL')
    res_scale:IntProperty(name = "Resolution Scale",default=100,min = 1)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'res_x',text = "X")
        layout.prop(self, 'res_y',text = "Y")
        layout.prop(self, 'res_scale',text = "%")

def register():
    bpy.utils.register_class(RSNodeResolutionInputNode)

def unregister():
    bpy.utils.unregister_class(RSNodeResolutionInputNode)