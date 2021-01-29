import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeImageFormatInputNode(RenderStackNode):
    bl_idname = "RSNodeImageFormatInputNode"
    bl_label = "Image Format"

    file_format: EnumProperty(
        name='File Format',
        items=[('PNG', 'PNG', '', 'IMAGE_DATA', 0),
               ('JPEG', 'JPEG', '', 'IMAGE_DATA', 1),
               ('OPEN_EXR_MULTILAYER', 'OpenEXR Multilayer', '', 'IMAGE_DATA', 2)],
        default='PNG', update=update_node)

    color_mode: EnumProperty(
        name='Color Mode',
        items=[('BW', 'BW', ''), ('RGB', 'RGB', ''), ('RGBA', 'RGBA', '')],
        default='RGBA', update=update_node)

    color_depth: EnumProperty(
        name='Color Depth',
        items=[('8', '8', ''), ('16', '16', ''), ('32', '32', '')],
        default='16', update=update_node)

    transparent: BoolProperty(default=False, name="Transparent", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, 'file_format', text='')
        col.prop(self, 'color_mode', text='')
        col.prop(self, 'color_depth', text='')
        col.prop(self, 'transparent')


def register():
    bpy.utils.register_class(RSNodeImageFormatInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeImageFormatInputNode)
