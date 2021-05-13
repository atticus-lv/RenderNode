import bpy
from bpy.props import *


def update_node(self, context):
    # transfer node socket value to node value
    self.node.node_dict[self.name] = self.value
    # update node tree
    self.node.update_parms()


class RenderNodeSocketObject(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketObject'
    bl_label = 'RenderNodeSocketObject'

    text: StringProperty(default='custom text')
    value: PointerProperty(type=bpy.types.Object, update=update_node)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)
        if self.value:
            row.operator('rsn.select_object', icon='RESTRICT_SELECT_OFF', text='').name = self.value.name
        # row.operator('rsn.pop_editor', text='', icon='PROPERTIES')

    def draw_color(self, context, node):
        return 1, 0.6, 0.3, 1


class RenderNodeSocketMaterial(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketMaterial'
    bl_label = 'RenderNodeSocketObject'

    text: StringProperty(default='custom text')
    value: PointerProperty(type=bpy.types.Material, update=update_node)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)
        # row.operator('rsn.pop_editor', text='', icon='PROPERTIES')

    def draw_color(self, context, node):
        return 0.6, 0.2, 0.2, 1


class RenderNodeSocketBool(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketBool'
    bl_label = 'RenderNodeSocketBool'

    text: StringProperty(default='custom text')
    value: BoolProperty(default=False, update=update_node)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)

    def draw_color(self, context, node):
        return 0.9, 0.7, 1.0, 1


class RenderNodeSocketInt(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketInt'
    bl_label = 'RenderNodeSocketInt'

    text: StringProperty(default='custom text')
    value: IntProperty(default=0, update=update_node)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)

    def draw_color(self, context, node):
        return 0, 0.9, 0.1, 1


class RenderNodeSocketFloat(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketFloat'
    bl_label = 'RenderNodeSocketFloat'

    text: StringProperty(default='custom text')
    value: FloatProperty(default=10, update=update_node)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)

    def draw_color(self, context, node):
        return 0.5, 0.5, 0.5, 1


class RenderNodeSocketString(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketString'
    bl_label = 'RenderNodeSocketString'

    text: StringProperty(default='custom text')
    value: StringProperty(default='', update=update_node)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)

    def draw_color(self, context, node):
        return 0.2, 0.5, 1.0, 1


class RenderNodeSocketColor(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketColor'
    bl_label = 'RenderNodeSocketColor'

    text: StringProperty(default='custom text')
    value: FloatVectorProperty(update=update_node, subtype='COLOR',
                               default=(1.0, 1.0, 1.0),
                               min=0.0, max=1.0)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)

    def draw_color(self, context, node):
        return 0.15, 1.0, 1.0, 1


class RenderNodeSocketVector(bpy.types.NodeSocket):
    bl_idname = 'RenderNodeSocketVector'
    bl_label = 'RenderNodeSocketVector'

    text: StringProperty(default='custom text')
    value: FloatVectorProperty(name='Vector', update=update_node)

    def draw(self, context, layout, node, text):
        row = layout.row(align=1)
        row.prop(self, 'value', text=self.text)

    def draw_color(self, context, node):
        return 0.5, 0.3, 1.0, 1


### old types ###
#################

class RSNodeSocketTaskSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketTaskSettings'
    bl_label = 'RSNodeSocketTaskSettings'

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            io = layout.operator('rsn.search_and_link', text=text, icon='ADD')
            io.node_name = node.name
            if self.is_output:
                io.output_id = int(self.path_from_id()[-2:-1])
                io.input_id = 666
            else:
                io.input_id = int(self.path_from_id()[-2:-1])
                io.output_id = 666
        else:
            layout.label(text=text)

    def draw_color(self, context, node):
        return 0.6, 0.6, 0.6, 1.0


class RSNodeSocketCamera(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketCamera'
    bl_label = 'RSNodeSocketCamera'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0, 0.8, 1.0, 1.0


class RSNodeSocketRenderSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderSettings'
    bl_label = 'RSNodeSocketRenderSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0, 1, 0.5, 1.0


class RSNodeSocketOutputSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketOutputSettings'
    bl_label = 'RSNod   eSocketOutputSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 1, 0.8, 0.2, 1.0


class RSNodeSocketRenderList(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderList'
    bl_label = 'RSNodeSocketRenderList'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return 0.95, 0.95, 0.95, 1.0


classes = (
    RSNodeSocketCamera,
    RSNodeSocketRenderSettings,
    RSNodeSocketOutputSettings,
    RSNodeSocketTaskSettings,
    RSNodeSocketRenderList,

    # new
    RenderNodeSocketObject,
    RenderNodeSocketMaterial,
    RenderNodeSocketBool,
    RenderNodeSocketInt,
    RenderNodeSocketFloat,
    RenderNodeSocketString,
    RenderNodeSocketColor,
    RenderNodeSocketVector,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
