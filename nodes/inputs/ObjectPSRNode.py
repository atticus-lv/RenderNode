import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def update_node(self, context):
    self.update()


class RSN_OT_FillOriginPSR(bpy.types.Operator):
    bl_idname = 'rsn.fill_origin_psr'
    bl_label = 'Fill Current PSR'

    object_name: StringProperty(default='')
    node_name: StringProperty()

    def execute(self, context):
        nt = context.space_data.edit_tree
        if self.object_name != '':
            obj = bpy.data.objects[self.object_name]
            node = nt.nodes[self.node_name]
            node.p = obj.location
            node.s = obj.scale
            node.r = obj.rotation_euler

        return {'FINISHED'}


class RSNodeObjectPSRNode(RenderStackNode):
    bl_idname = 'RSNodeObjectPSRNode'
    bl_label = 'Object PSR'

    object: PointerProperty(type=bpy.types.Object, name='Object', update=update_node)

    use_p: BoolProperty(name='P', default=True, update=update_node)
    use_s: BoolProperty(name='S', update=update_node)
    use_r: BoolProperty(name='R', update=update_node)

    p: FloatVectorProperty(name='Location', subtype='TRANSLATION', update=update_node)
    s: FloatVectorProperty(name='Scale', default=(1, 1, 1), update=update_node)
    r: FloatVectorProperty(name='Rotation', subtype='EULER', update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_split = 1
        layout.use_property_decorate = False

        col = layout.column(align=1)
        col.prop(self, "object")

        col.separator(factor=0.5)
        row = col.row(align=True)

        row.prop(self, "use_p")
        row.prop(self, "use_s")
        row.prop(self, "use_r")

        col.separator(factor=0.5)
        if self.use_p: col.prop(self, 'p')

        col.separator(factor=0.5)
        if self.use_s: col.prop(self, 's')

        col.separator(factor=0.5)
        if self.use_r: col.prop(self, 'r')

        if self.object:
            fill = col.operator("rsn.fill_origin_psr")
            fill.object_name = self.object.name if self.object else ''
            fill.node_name = self.name

    def draw_buttons_ext(self, context, layout):
        pass


def register():
    bpy.utils.register_class(RSNodeObjectPSRNode)
    bpy.utils.register_class(RSN_OT_FillOriginPSR)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectPSRNode)
    bpy.utils.unregister_class(RSN_OT_FillOriginPSR)
