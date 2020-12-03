import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSFileScriptsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSFileScriptsNode'
    bl_label = 'Scripts File'

    file:PointerProperty(type=bpy.types.Text,name = "Scripts file")

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Script")
        self.width = 200


    def draw_buttons(self, context, layout):
        layout.prop(self,"file",text="")



def register():
    bpy.utils.register_class(RSFileScriptsNode)

def unregister():
    bpy.utils.unregister_class(RSFileScriptsNode)