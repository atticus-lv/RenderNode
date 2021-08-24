import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def poll_object(self, object):
    return object.type in {'MESH', 'CURVE', 'VOLUME'}


def update_slot_index(self, context):
    if self.object:
        if self.slot_index > len(self.object.material_slots) - 1:
            self.slot_index = len(self.object.material_slots) - 1
    self.execute_tree()


def update_node(self, context):
    self.execute_tree()


class RenderNodeObjectMaterial(RenderNodeBase):
    bl_idname = 'RenderNodeObjectMaterial'
    bl_label = 'Object Material'

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_input('RenderNodeSocketInt', 'slot_index', 'Slot Index')
        self.create_input('RenderNodeSocketMaterial', 'material', 'Mat')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")


    def process(self,context,id,path):
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
    bpy.utils.register_class(RenderNodeObjectMaterial)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectMaterial)
