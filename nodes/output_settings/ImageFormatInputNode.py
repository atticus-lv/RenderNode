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

    def get_data(self):
        task_data = {}
        if self.file_format == "JPEG":
            if self.color_mode == "RGBA":
                self.color_mode = "RGB"
            if self.color_depth in ("16", "32"):
                self.color_depth = "8"

        elif self.file_format == "PNG":
            if self.color_depth == '32':
                self.color_depth = "16"

        elif self.file_format == "OPEN_EXR_MULTILAYER":
            if self.color_depth == "8":
                self.color_depth = "16"

        task_data['color_mode'] = self.color_mode
        task_data['color_depth'] = self.color_depth
        task_data['file_format'] = self.file_format
        task_data['transparent'] = self.transparent
        return task_data


def register():
    bpy.utils.register_class(RSNodeImageFormatInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeImageFormatInputNode)
