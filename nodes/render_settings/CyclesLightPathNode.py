import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeCyclesLightPathNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCyclesLightPathNode'
    bl_label = 'Cycles Light Path'

    max_bounces: IntProperty(default=12, update=update_node)
    diffuse_bounces: IntProperty(default=4, update=update_node)
    glossy_bounces: IntProperty(default=4, update=update_node)
    transparent_max_bounces: IntProperty(default=8, update=update_node)
    transmission_bounces: IntProperty(default=12, update=update_node)
    volume_bounces: IntProperty(default=0, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, "max_bounces", text="Total")

        col = layout.column(align=True)
        col.prop(self, "diffuse_bounces", text="Diffuse")
        col.prop(self, "glossy_bounces", text="Glossy")
        col.prop(self, "transparent_max_bounces", text="Transparency")
        col.prop(self, "transmission_bounces", text="Transmission")
        col.prop(self, "volume_bounces", text="Volume")


def register():
    bpy.utils.register_class(RSNodeCyclesLightPathNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCyclesLightPathNode)
