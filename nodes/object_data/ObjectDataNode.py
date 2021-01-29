import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeObjectDataNode(RenderStackNode):
    bl_idname = 'RSNodeObjectDataNode'
    bl_label = 'Object Data'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)
    data_path: StringProperty(name='Data Path', update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = False

        layout.prop(self, "object")
        layout.prop(self, 'data_path')
        if self.object and hasattr(self.object.data, self.data_path):
            layout.prop(self.object.data, self.data_path)



def register():
    bpy.utils.register_class(RSNodeObjectDataNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectDataNode)
