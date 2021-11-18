import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetRenderSlot(RenderNodeBase):
    bl_idname = 'RenderNodeSetRenderSlot'
    bl_label = 'Set Render Slot'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_input('RenderNodeSocketInt', 'slot_index', 'Slot', default_value=1)

        self.create_output('RenderNodeSocketTask', 'task', 'Task')


    def process(self,context,id,path):
        self.process_task()

        render_result = bpy.data.images.get('Render Result')
        if not render_result: return None

        if self.inputs['slot_index'].get_value() < 1:
            self.inputs['slot_index'].set_value(1)

        if self.inputs['slot_index'].get_value() > len(render_result.render_slots):
            self.inputs['slot_index'].set_value(len(render_result.render_slots))

        render_result.render_slots.active_index = self.inputs['slot_index'].get_value()


def register():
    bpy.utils.register_class(RenderNodeSetRenderSlot)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetRenderSlot)
