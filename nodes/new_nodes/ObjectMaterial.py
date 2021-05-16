import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def poll_object(self, object):
    return object.type in {'MESH', 'CURVE', 'VOLUME'}


def update_slot_index(self, context):
    if self.object:
        if self.slot_index > len(self.object.material_slots) - 1:
            self.slot_index = len(self.object.material_slots) - 1
    self.update_parms()


def update_node(self, context):
    self.update_parms()


class RenderNodeObjectMaterial(RenderStackNode):
    bl_idname = 'RenderNodeObjectMaterial'
    bl_label = 'Object Material +'

    def init(self, context):
        self.create_prop('RenderNodeSocketObject', 'object', 'Object')
        self.create_prop('RenderNodeSocketInt', 'slot_index', 'Slot Index')
        self.create_prop('RenderNodeSocketMaterial', 'material', 'Mat')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def process(self):
        self.store_data()

        ob = self.node_dict['object']
        if ob:
            try:
                curr_slot = ob.material_slots[self.node_dict['slot_index']]
                self.compare(curr_slot, 'material', self.node_dict['material'])
            except Exception as e:
                print(e)


def register():
    bpy.utils.register_class(RenderNodeObjectMaterial)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectMaterial)
