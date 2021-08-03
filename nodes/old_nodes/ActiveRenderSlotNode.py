import bpy
from bpy.props import IntProperty
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.update_parms()


class RSNodeActiveRenderSlotNode(RenderNodeBase):
    bl_idname = "RSNodeActiveRenderSlotNode"
    bl_label = 'Render Slot'

    active_slot_index: IntProperty(default=0, min=0, max=7, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'active_slot_index', text="Render Slot")

    def get_data(self):
        task_data = {}
        task_data['render_slot'] = self.active_slot_index
        return task_data

def register():
    bpy.utils.register_class(RSNodeActiveRenderSlotNode)


def unregister():
    bpy.utils.unregister_class(RSNodeActiveRenderSlotNode)