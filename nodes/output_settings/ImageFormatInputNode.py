import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class ImageFormatInputNode(RenderStackNode):
    bl_idname = "ImageFormatInputNode"
    bl_label = "Image Format"

    file_format: EnumProperty(
        name='File Format',
        items=[('PNG', 'PNG', '', 'IMAGE_DATA', 0),
               ('JPEG', 'JPEG', '', 'IMAGE_DATA', 1),
               ('OPEN_EXR_MULTILAYER', 'OpenEXR Multilayer', '', 'IMAGE_DATA', 2)],
        default='PNG')

    color_mode: EnumProperty(
        name='Color Mode',
        items=[('BW', 'BW', ''), ('RGB', 'RGB', ''), ('RGBA', 'RGBA', '')],
        default='RGBA', )

    color_depth: EnumProperty(
        name='Color Depth',
        items=[('8', '8', ''), ('16', '16', ''), ('32', '32', '')],
        default='16', )

    transparent: BoolProperty(default=False, name="Transparent")

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'file_format', text='')
        layout.prop(self, 'color_mode', text='')
        layout.prop(self, 'color_depth', text='')
        layout.prop(self, 'transparent')


def register():
    bpy.utils.register_class(ImageFormatInputNode)


def unregister():
    bpy.utils.unregister_class(ImageFormatInputNode)
