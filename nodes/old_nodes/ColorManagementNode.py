import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RSNodeColorManagementNode(RenderNodeBase):
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
                                 default='Filmic', update=update_node)

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
                       default='None', update=update_node)

    ev: FloatProperty(name="Exposure Value", default=0, soft_min=-3, soft_max=3, update=update_node)
    gamma: FloatProperty(name="Gamma", default=1.0, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        col = layout.column(align=1)
        col.prop(self, 'view_transform')
        col.prop(self, 'look')

        col.prop(self, 'ev', slider=1)
        col.prop(self, 'gamma')

    def get_data(self):
        task_data = {}
        task_data['view_transform'] = self.view_transform
        task_data['look'] = self.look
        task_data['ev'] = self.ev
        task_data['gamma'] = self.gamma
        return task_data


def register():
    bpy.utils.register_class(RSNodeColorManagementNode)


def unregister():
    bpy.utils.unregister_class(RSNodeColorManagementNode)
