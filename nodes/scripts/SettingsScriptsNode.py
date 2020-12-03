import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSSettingsScriptsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSSettingsScriptsNode'
    bl_label = 'Scripts'

    code:StringProperty(name = 'Code to execute',default='')

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Script")
        self.width = 200


    def draw_buttons(self, context, layout):
        layout.prop(self,"code",text="")



def register():
    bpy.utils.register_class(RSSettingsScriptsNode)

def unregister():
    bpy.utils.unregister_class(RSSettingsScriptsNode)