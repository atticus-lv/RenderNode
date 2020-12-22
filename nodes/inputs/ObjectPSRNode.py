import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeObjectPSRNode(RenderStackNode):
    bl_idname = 'RSNodeObjectPSRNode'
    bl_label = 'Object PSR'

    object: PointerProperty(type=bpy.types.Object, name='Object')

    use_p: BoolProperty(name='P')
    use_s: BoolProperty(name='S')
    use_r: BoolProperty(name='R')

    p: FloatVectorProperty(name='Location',subtype = 'TRANSLATION')
    s: FloatVectorProperty(name='Scale',default=(1,1,1))
    r: FloatVectorProperty(name='Rotation',subtype = 'EULER')

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = False

        layout.prop(self, "object")
        row = layout.row(align=True)
        row.prop(self, "use_p")
        row.prop(self, "use_s")
        row.prop(self, "use_r")

        if self.use_p: layout.prop(self, 'p')
        if self.use_s: layout.prop(self, 's')
        if self.use_r: layout.prop(self, 'r')

    def draw_buttons_ext(self, context, layout):
        pass


def register():
    bpy.utils.register_class(RSNodeObjectPSRNode)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectPSRNode)
