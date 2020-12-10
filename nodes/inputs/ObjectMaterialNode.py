import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def poll_object(self, object):
    return object.type in {'MESH', 'CURVE', 'VOLUME'}


class RSNodeObjectMaterialNode(RenderStackNode):
    bl_idname = 'RSNodeObjectMaterialNode'
    bl_label = 'Object Material'

    object: PointerProperty(type=bpy.types.Object, poll=poll_object, name='Object')

    old_material: PointerProperty(type=bpy.types.Material, name='Old Mat')
    new_material: PointerProperty(type=bpy.types.Material, name='New Mat')

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 175

    def draw_buttons(self, context, layout):
        layout.prop(self, "object")
        layout.prop(self, 'old_material')
        layout.prop(self, 'new_material')

    def draw_buttons_ext(self, context, layout):
        pass


def register():
    bpy.utils.register_class(RSNodeObjectMaterialNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectMaterialNode)
