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
               ('TIFF', 'TIFF', '', 'IMAGE_DATA', 2),
               ('OPEN_EXR', 'OpenEXR', '', 'IMAGE_DATA', 3),
               ('OPEN_EXR_MULTILAYER', 'OpenEXR Multilayer', '', 'IMAGE_DATA', 4),
               ],
        default='OPEN_EXR', update=update_node)

    color_mode: EnumProperty(
        name='Color Mode',
        items=[('BW', 'BW', ''), ('RGB', 'RGB', ''), ('RGBA', 'RGBA', '')],
        default='RGBA', update=update_node)

    color_depth: EnumProperty(
        name='Color Depth',
        items=[('8', '8', ''), ('16', '16', ''), ('32', '32', '')],
        default='16', update=update_node)

    use_preview: BoolProperty(name='Save Preview', default=False)
    transparent: BoolProperty(default=False, name="Transparent(Built in Engines Only)", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, 'file_format', text='')
        col.prop(self, 'color_mode', text='')
        col.prop(self, 'color_depth', text='')
        col.prop(self, 'transparent')
        if self.file_format in {"OPEN_EXR_MULTILAYER,OPEN_EXR"}:
            col.prop(self, 'use_preview')

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

        task_data['color_mode'] = self.color_mode
        task_data['color_depth'] = self.color_depth
        task_data['file_format'] = self.file_format
        task_data['use_preview'] = self.use_preview
        task_data['transparent'] = self.transparent
        return task_data


def register():
    bpy.utils.register_class(RSNodeImageFormatInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeImageFormatInputNode)
