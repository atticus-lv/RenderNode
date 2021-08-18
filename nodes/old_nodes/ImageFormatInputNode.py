import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RSNodeImageFormatInputNode(RenderNodeBase):
    bl_idname = "RSNodeImageFormatInputNode"
    bl_label = "Image Format"

    file_format: EnumProperty(
        name='File Format',
        items=[('PNG', 'PNG', '', 'IMAGE_DATA', 0),
               ('JPEG', 'JPEG', '', 'IMAGE_DATA', 1),
               ('TIFF', 'TIFF', '', 'IMAGE_DATA', 2),
               ('OPEN_EXR', 'OpenEXR', '', 'IMAGE_DATA', 3),
               ('OPEN_EXR_MULTILAYER', 'OpenEXR Multilayer', '', 'IMAGE_DATA', 4),
               ],
        default='OPEN_EXR', update=update_node)

    color_mode: EnumProperty(
        name='Color',
        items=[('BW', 'BW', ''), ('RGB', 'RGB', ''), ('RGBA', 'RGBA', '')],
        default='RGBA', update=update_node)

    color_depth: EnumProperty(
        name='Color Depth',
        items=[('8', '8', ''), ('16', '16', ''), ('32', '32', '')],
        default='16', update=update_node)
    # exr file
    use_preview: BoolProperty(name='Save Preview', default=False)
    # jpg file
    quality: IntProperty(name='Quality', default=90, min=0, max=100,subtype='PERCENTAGE')
    # png file
    compression: IntProperty(name="Compression", default=15, min=0, max=100,subtype='PERCENTAGE')

    transparent: BoolProperty(default=False, name="Transparent", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.use_property_decorate = 0
        layout.use_property_split = 1
        col = layout.column(align=1)
        col.prop(self, 'file_format')
        col.prop(self, 'color_mode')
        col.prop(self, 'color_depth')

        if self.file_format in {'OPEN_EXR_MULTILAYER', 'OPEN_EXR'}:
            col.prop(self, 'use_preview')
        if self.file_format == "PNG":
            col.prop(self, 'compression',slider= 1)
        if self.file_format == "JPEG":
            col.prop(self, 'quality',slider= 1)

        col.prop(self, 'transparent')

    def get_data(self):
        task_data = {}
        if self.file_format == "JPEG":
            if self.color_mode == "RGBA":
                self.color_mode = "RGB"
            if self.color_depth in ("16", "32"):
                self.color_depth = "8"

        elif self.file_format in {'TIFF', "PNG"}:
            if self.color_depth == '32':
                self.color_depth = "16"

        elif self.file_format in {'OPEN_EXR_MULTILAYER', 'OPEN_EXR'}:
            if self.color_depth == "8":
                self.color_depth = "16"

        task_data_obj = {}
        task_data_obj['color_mode'] = self.color_mode
        task_data_obj['color_depth'] = self.color_depth
        task_data_obj['file_format'] = self.file_format
        task_data_obj['compression'] = self.compression
        task_data_obj['quality'] = self.quality
        task_data_obj['use_preview'] = self.use_preview
        task_data_obj['transparent'] = self.transparent

        task_data['image_settings'] = task_data_obj
        return task_data


def register():
    bpy.utils.register_class(RSNodeImageFormatInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeImageFormatInputNode)
