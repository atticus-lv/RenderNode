import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def poll_object(self, object):
    return object.type in {'MESH', 'CURVE', 'VOLUME'}


def update_slot_index(self, context):
    if self.object:
        if self.slot_index > len(self.object.material_slots) - 1:
            self.slot_index = len(self.object.material_slots) - 1


class RSNodeObjectMaterialNode(RenderStackNode):
    bl_idname = 'RSNodeObjectMaterialNode'
    bl_label = 'Object Material'

    object: PointerProperty(type=bpy.types.Object, poll=poll_object, name='Object')

    slot_index: IntProperty(min=0, default=0, name="Slot index", update=update_slot_index)
    new_material: PointerProperty(type=bpy.types.Material, name='New Mat')

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = False
        layout.prop(self, "object")
        layout.prop(self, 'slot_index', text='Slot')
        layout.prop(self, 'new_material', text='Material')

    def draw_buttons_ext(self, context, layout):
        pass


def register():
    bpy.utils.register_class(RSNodeObjectMaterialNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectMaterialNode)
