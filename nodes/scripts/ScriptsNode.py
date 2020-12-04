import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSScriptsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSScriptsNode'
    bl_label = 'Scripts'

    code:StringProperty(name = 'Code to execute',default='')
    file: PointerProperty(type=bpy.types.Text, name="Scripts file")

    type:EnumProperty(
        items=[
            ('SINGLE','Single',''),('FILE','File','')
        ]
    )

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200


    def draw_buttons(self, context, layout):
        if self.type == 'SINGLE':
            layout.prop(self,"code",text="")
        else:
            layout.prop(self, "file", text="")



def register():
    bpy.utils.register_class(RSScriptsNode)

def unregister():
    bpy.utils.unregister_class(RSScriptsNode)