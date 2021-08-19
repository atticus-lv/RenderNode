import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RSNodeCyclesLightPathNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodeCyclesLightPathNode'
    bl_label = 'Cycles Light Path'

    max_bounces: IntProperty(default=12, update=update_node)
    diffuse_bounces: IntProperty(default=4, update=update_node)
    glossy_bounces: IntProperty(default=4, update=update_node)
    transparent_max_bounces: IntProperty(default=8, update=update_node)
    transmission_bounces: IntProperty(default=12, update=update_node)
    volume_bounces: IntProperty(default=0, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, "max_bounces", text="Total")

        col = layout.column(align=True)
        col.prop(self, "diffuse_bounces", text="Diffuse")
        col.prop(self, "glossy_bounces", text="Glossy")
        col.prop(self, "transparent_max_bounces", text="Transparency")
        col.prop(self, "transmission_bounces", text="Transmission")
        col.prop(self, "volume_bounces", text="Volume")

    def process(self, context, id, path):
        task_data = self.get_data()
        if 'cycles_light_path' in task_data:
            for key, value in task_data['cycles_light_path'].items():
                self.compare(context.scene.cycles, key, value)

    def get_data(self):
        task_data = {}
        task_data['cycles_light_path'] = {
            "max_bounces"            : self.max_bounces,
            "diffuse_bounces"        : self.diffuse_bounces,
            "glossy_bounces"         : self.glossy_bounces,
            "transparent_max_bounces": self.transparent_max_bounces,
            "transmission_bounces"   : self.transmission_bounces,
            "volume_bounces"         : self.volume_bounces,
        }

        return task_data


def register():
    bpy.utils.register_class(RSNodeCyclesLightPathNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCyclesLightPathNode)
