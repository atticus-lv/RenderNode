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
    bl_label = 'Object Material'

    object: PointerProperty(type=bpy.types.Object, poll=poll_object, name='Object', update=update_node)

    slot_index: IntProperty(min=0, default=0, name="Slot index", update=update_slot_index)
    new_material: PointerProperty(type=bpy.types.Material, name='New Mat', update=update_node)

    def init(self, context):
        self.create_prop('RenderNodeSocketObject', 'object', 'Object')
        self.create_prop('RenderNodeSocketInt', 'slot_index', 'Slot Index')
        self.create_prop('RenderNodeSocketMaterial', 'new_material', 'New Mat')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        pass
        # layout.use_property_split = 1
        # layout.use_property_decorate = 0
        # col = layout.column(align=1)
        #
        # row = col.row(align=1)
        # row.prop(self, "object")
        # if self.object:
        #     row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.object.name
        #
        # col.prop(self, 'slot_index', text='Slot')
        # col.prop(self, 'new_material', text='Material')

    def get_data(self):
        task_data_obj = {}
        if self.inputs['object'].object is not None and self.inputs['new_material'].material is not None:
            task_data_obj[self.name] = {'object'      : f"bpy.data.objects['{self.inputs['object'].object.name}']",
                                        'slot_index'  : self.inputs['slot_index'].int,
                                        'new_material': self.inputs['new_material'].material.name}
        # print(task_data_obj)
        return task_data_obj


def register():
    bpy.utils.register_class(RenderNodeObjectMaterial)


def unregister():
    bpy.utils.unregister_class(RenderNodeObjectMaterial)
