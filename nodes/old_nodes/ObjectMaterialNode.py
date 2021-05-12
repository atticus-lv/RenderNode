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

    object: PointerProperty(type=bpy.types.Object, poll=poll_object, name='Object', update=update_node)

    slot_index: IntProperty(min=0, default=0, name="Slot index", update=update_slot_index)
    new_material: PointerProperty(type=bpy.types.Material, name='New Mat', update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        col = layout.column(align=1)

        row = col.row(align=1)
        row.prop(self, "object")
        if self.object:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.object.name

        col.prop(self, 'slot_index', text='Slot')
        col.prop(self, 'new_material', text='Material')

    def get_data(self):
        task_data_obj = {}
        if self.object and self.new_material:
            task_data_obj[self.name] = {'object'   : f"bpy.data.objects['{self.object.name}']",
                                        'slot_index'  : self.slot_index,
                                        'new_material': self.new_material.name}
        return task_data_obj


def register():
    bpy.utils.register_class(RSNodeObjectMaterialNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectMaterialNode)
