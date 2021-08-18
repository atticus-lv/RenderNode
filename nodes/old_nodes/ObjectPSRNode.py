import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


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


class RSNodeObjectPSRNode(RenderNodeBase):
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

        row = col.row(align=1)
        row.prop(self, "object")
        if self.object:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.object.name

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

    def get_data(self):
        task_data_obj = {}
        if self.object and True in {self.use_p, self.use_s, self.use_r}:
            d = {'object': f"bpy.data.objects['{self.object.name}']"}
            if self.use_p:
                d['location'] = list(self.p)
            if self.use_s:
                d['scale'] = list(self.s)
            if self.use_r:
                d['rotation'] = list(self.r)
            task_data_obj[self.name] = d

        return task_data_obj


def register():
    bpy.utils.register_class(RSNodeObjectPSRNode)
    bpy.utils.register_class(RSN_OT_FillOriginPSR)


def unregister():
    bpy.utils.unregister_class(RSNodeObjectPSRNode)
    bpy.utils.unregister_class(RSN_OT_FillOriginPSR)
