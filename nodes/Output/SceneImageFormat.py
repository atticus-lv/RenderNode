import bpy
from bpy.props import *

from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.update_parms()


class RenderNodeSceneImageFormat(RenderNodeBase):
    bl_idname = "RenderNodeSceneImageFormat"
    bl_label = "Scene Image Format"

    file_format: EnumProperty(name='File Format',
                              items=[('BMP', 'BMP', ''), ('IRIS', 'IRIS', ''), ('PNG', 'PNG', ''), ('JPEG', 'JPEG', ''),
                                     ('JPEG2000', 'JPEG2000', ''), ('TARGA', 'TARGA', ''),
                                     ('TARGA_RAW', 'TARGA_RAW', ''), ('CINEON', 'CINEON', ''), ('DPX', 'DPX', ''),
                                     ('OPEN_EXR_MULTILAYER', 'OPEN_EXR_MULTILAYER', ''), ('OPEN_EXR', 'OPEN_EXR', ''),
                                     ('HDR', 'HDR', ''), ('TIFF', 'TIFF', '')],
                              default='PNG',
                              update=update_node)

    # png
    compression: IntProperty(name='Compression',
                             default=15, min=0, max=100,
                             update=update_node)
    # jpg / jpg2000
    quality: IntProperty(name='Quality',
                         default=90, min=0, max=100,
                         update=update_node)
    # jpeg2000
    jpeg2k_tiff_codec: EnumProperty(name='Codec',
                                    items=[('JP2', 'JP2', ''), ('J2K', 'J2K', '')],
                                    default='JP2',
                                    update=update_node)

    use_jpeg2k_cinema_preset: BoolProperty(name='Cinema',
                                           update=update_node)
    use_jpeg2k_cinema_48: BoolProperty(name='Cinema_48',
                                       update=update_node)
    use_jpeg2k_ycc: BoolProperty(name='YCC',
                                 update=update_node)
    # cineon
    use_cineon_log: BoolProperty(name='Log',
                                 description='Convert to logarithmic color space',
                                 update=update_node)

    # exr
    exr_codec: EnumProperty(name='Codec',
                            items=[('NONE', 'NONE', ''), ('PXR24', 'PXR24', ''), ('ZIP', 'ZIP', ''), ('PIZ', 'PIZ', ''),
                                   ('RLE', 'RLE', ''), ('ZIPS', 'ZIPS', ''), ('B44', 'B44', ''), ('B44A', 'B44A', ''),
                                   ('DWAA', 'DWAA', '')],
                            default='ZIPS',
                            update=update_node)
    use_preview: BoolProperty(name='Preview',
                              update=update_node)
    # muti exr
    use_zbuffer: BoolProperty(name='Z Buffer',
                              update=update_node)
    # tiff
    tiff_codec: EnumProperty(name='Compression',
                             description='Compression mode for TIFF',
                             items=[('NONE', 'NONE', ''), ('DEFLATE', 'DEFLATE', ''), ('LZW', 'LZW', ''),
                                    ('PACKBITS', 'PACKBITS', '')],
                             update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.use_property_split = 1
        col.use_property_decorate = 0

        col.prop(self, 'file_format', icon='FILE_IMAGE')
        row = col.row(align=1)
        row.prop(self, 'color_mode', expand=1)

        if self.file_format in ['PNG', 'TIFF',
                                'JPEG2000',
                                'DPX', 'OPEN_EXR_MULTILAYER', 'OPEN_EXR']:
            row = col.row(align=1)
            row.prop(self, 'color_depth', expand=1)

        # extra
        if self.file_format == 'PNG':
            col.prop(self, 'compression', slider=1)

        elif self.file_format in ['JPEG', 'JPEG2000']:
            col.prop(self, 'quality', slider=1)
            if self.file_format == 'JPEG2000':
                col.prop(self, 'use_jpeg2k_cinema_preset')
                col.prop(self, 'use_jpeg2k_cinema_48')
                col.prop(self, 'use_jpeg2k_cinema_48')

        elif self.file_format == 'CINEON':
            col.prop(self, 'use_cineon_log')
        elif self.file_format in ['OPEN_EXR_MULTILAYER', 'OPEN_EXR']:
            col.prop(self, 'exr_codec')
            col.prop(self, 'use_preview')
            if self.file_format == 'OPEN_EXR_MULTILAYER':
                col.prop(self, 'use_zbuffer')
        elif self.file_format == 'TIFF':
            col.prop(self, 'tiff_codec')

    def process(self):
        attr_list = ['file_format',
                     'compression',
                     'quality',
                     'jpeg2k_tiff_codec', 'use_jpeg2k_cinema_preset', 'use_jpeg2k_cinema_48',
                     'use_jpeg2k_ycc',
                     'use_cineon_log',
                     'exr_codec', 'use_preview', 'use_zbuffer', 'tiff_codec']

        for attr in attr_list:
            try:
                self.compare(bpy.context.scene.render.image_settings, attr, getattr(self, attr))
            except Exception as e:
                print(e)

    def enum_color_mode(self, context):
        if self.file_format in ['BMP', 'JPEG', 'CINEON', 'HDR']:
            return [('BW', 'BW', ''), ('RGB', 'RGB', '')]
        else:
            return [('BW', 'BW', ''), ('RGB', 'RGB', ''), ('RGBA', 'RGBA', '')]

    def enum_color_depth(self, context):
        if self.file_format in ['PNG', 'TIFF']:
            return [('8', '8', ''), ('16', '16', '')]
        elif self.file_format in ['JPEG2000']:
            return [('8', '8', ''), ('12', '12', ''), ('16', '16', '')]
        elif self.file_format in ['DPX']:
            return [('8', '8', ''), ('10', '10', ''), ('12', '12', ''), ('16', '16', '')]
        elif self.file_format in ['OPEN_EXR_MULTILAYER', 'OPEN_EXR']:
            return [('16', 'Float(Half)', ''), ('32', 'Float(Full)', '')]
        else:
            return []

    temp_color_mode = enum_color_mode
    temp_color_depth = enum_color_depth

    color_mode: EnumProperty(name='Color Mode',
                             items=temp_color_mode,
                             update=update_node)
    color_depth: EnumProperty(name='Color Depth',
                              items=temp_color_depth,
                              update=update_node)


def register():
    bpy.utils.register_class(RenderNodeSceneImageFormat)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneImageFormat)
