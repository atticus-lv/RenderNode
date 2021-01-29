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

class RSNodeObjectMaterialNode(RenderStackNode):
    bl_idname = 'RSNodeObjectMaterialNode'
    bl_label = 'Object Material'

    object: PointerProperty(type=bpy.types.Object, poll=poll_object, name='Object',update=update_node)

    slot_index: IntProperty(min=0, default=0, name="Slot index", update=update_slot_index)
    new_material: PointerProperty(type=bpy.types.Material, name='New Mat',update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        col = layout.column(align=1)
        col.prop(self, "object")
        col.prop(self, 'slot_index', text='Slot')
        col.prop(self, 'new_material', text='Material')



def register():
    bpy.utils.register_class(RSNodeObjectMaterialNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectMaterialNode)
