import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeLuxcoreWorldSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeLuxcoreWorldSettingsNode'
    bl_label = 'Luxcore World Settings'

    light: EnumProperty(items=[
        ('sky2', 'Sky', ''), ('infinite', 'HDRI', ''), ('constantinfinite', "Flat Color",''), ('none', 'None', '')
    ], default="infinite")

    image: PointerProperty(type=bpy.types.Image)
    gamma: FloatProperty(default=1.0)
    rotation: FloatProperty(default=0, subtype="ANGLE")

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")
        self.width = 250

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.prop(self,'light',expand= 1)
        if self.light == 'infinite':
            layout.prop(self,'image')
            layout.prop(self,'gamma')
            layout.prop(self,'rotation')


def register():
    bpy.utils.register_class(RSNodeLuxcoreWorldSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeLuxcoreWorldSettingsNode)
