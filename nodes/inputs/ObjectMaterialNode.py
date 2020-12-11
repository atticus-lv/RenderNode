import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def poll_object(self, object):
    return object.type in {'MESH', 'CURVE', 'VOLUME'}


class RSN_OT_MaterialSwitch(bpy.types.Operator):
    bl_idname = 'rsn.material_switch'
    bl_label = 'Switch Material'

    node_name: StringProperty(name='RSNodeObjectMaterialNode', default='')

    def execute(self, context):
        if self.node_name != '':
            nt = bpy.context.space_data.edit_tree
            node = nt.nodes[self.node_name]
            if node.old_material and node.new_material:
                temp = node.new_material
                node.new_material = node.old_material
                node.old_material = temp

        return {"FINISHED"}


class RSNodeObjectMaterialNode(RenderStackNode):
    bl_idname = 'RSNodeObjectMaterialNode'
    bl_label = 'Object Material'

    object: PointerProperty(type=bpy.types.Object, poll=poll_object, name='Object')

    old_material: PointerProperty(type=bpy.types.Material, name='Old Mat')
    new_material: PointerProperty(type=bpy.types.Material, name='New Mat')

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 225

    def draw_buttons(self, context, layout):
        layout.prop(self, "object")
        row = layout.row(align=1)
        row.prop(self, 'old_material', text='')
        row.label(text="", icon='TRIA_RIGHT')
        row.prop(self, 'new_material', text='')
        layout.operator("rsn.material_switch", icon='ARROW_LEFTRIGHT').node_name = self.name

    def draw_buttons_ext(self, context, layout):
        pass


def register():
    bpy.utils.register_class(RSNodeObjectMaterialNode)
    bpy.utils.register_class(RSN_OT_MaterialSwitch)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectMaterialNode)
    bpy.utils.unregister_class(RSN_OT_MaterialSwitch)
