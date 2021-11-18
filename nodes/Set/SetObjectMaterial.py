import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RenderNodeSetObjectMaterial(RenderNodeBase):
    bl_idname = 'RenderNodeSetObjectMaterial'
    bl_label = 'Set Object Material'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')
        self.create_input('RenderNodeSocketObject', 'object', '')
        self.create_input('RenderNodeSocketInt', 'slot_index', 'Slot Index')
        self.create_input('RenderNodeSocketMaterial', 'material', 'Mat')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')


    def process(self,context,id,path):
        if not self.process_task():return
        ob = self.inputs['object'].get_value()
        index = self.inputs['slot_index'].get_value()
        mat = self.inputs['material'].get_value()

        if ob:
            try:
                curr_slot = ob.material_slots[index]
                self.compare(curr_slot, 'material', mat)
            except Exception as e:
                raise ValueError('Slot index or Object error')


def register():
    bpy.utils.register_class(RenderNodeSetObjectMaterial)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetObjectMaterial)
