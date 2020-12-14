import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeColorManagementNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeColorManagementNode'
    bl_label = 'Color Management'

    view_transform: EnumProperty(name='View Transform',
                                 items=[
                                     ('False Color', 'False Color', ''),
                                     ('Raw', 'Raw', ''),
                                     ('Filmic Log', 'Filmic Log', ''),
                                     ('Filmic', 'Filmic', ''),
                                     ('Standard', 'Standard', '')],
                                 default='Filmic')

    look: EnumProperty(name='Look',
                       items=[
                           ('Very Low Contrast', 'Very Low Contrast', ''),
                           ('Low Contrast', 'Low Contrast', ''),
                           ('Medium Low Contrast', 'Medium Low Contrast', ''),
                           ('Medium Contrast', 'Medium Contrast', ''),
                           ('Medium High Contrast', 'Medium High Contrast', ''),
                           ('High Contrast', 'High Contrast', ''),
                           ('Very High Contrast', 'Very High Contrast', ''),
                           ('None', 'None', '')],
                       default='None')

    ev: FloatProperty(name="Exposure Value", default=0, soft_min=-3, soft_max=3)
    gamma: FloatProperty(name="Gamma", default=1.0)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        layout.prop(self, 'view_transform')
        layout.prop(self, 'look')

        layout.prop(self, 'ev', slider=1)
        layout.prop(self, 'gamma')


def register():
    bpy.utils.register_class(RSNodeColorManagementNode)


def unregister():
    bpy.utils.unregister_class(RSNodeColorManagementNode)
