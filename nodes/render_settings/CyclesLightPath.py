import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RenderNodeCyclesLightPath(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeCyclesLightPath'
    bl_label = 'Cycles Light Path'

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'max_bounces', 'Total', default_value=12)
        self.create_input('RenderNodeSocketInt', 'diffuse_bounces', 'Diffuse', default_value=4)
        self.create_input('RenderNodeSocketInt', 'glossy_bounces', 'Glossy', default_value=4)
        self.create_input('RenderNodeSocketInt', 'transparent_max_bounces', 'Transparency', default_value=8)
        self.create_input('RenderNodeSocketInt', 'transmission_bounces', 'Transmission', default_value=12)
        self.create_input('RenderNodeSocketInt', 'volume_bounces', 'Volume', default_value=0)

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def process(self, context, id, path):
        for input in self.inputs:
            key = input.name
            value = input.get_value()
            compare(bpy.context.scene.cycles, key, value)



def register():
    bpy.utils.register_class(RenderNodeCyclesLightPath)


def unregister():
    bpy.utils.unregister_class(RenderNodeCyclesLightPath)
