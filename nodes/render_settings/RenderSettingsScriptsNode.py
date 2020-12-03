import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RenderSettingsScriptsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RenderSettingsScriptsNode'
    bl_label = 'Render Scripts'

    code:StringProperty(name = 'Code to execute',default='')

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Script")
        self.width = 200


    def draw_buttons(self, context, layout):
        layout.prop(self,"code",text="")



def register():
    bpy.utils.register_class(RenderSettingsScriptsNode)

def unregister():
    bpy.utils.unregister_class(RenderSettingsScriptsNode)