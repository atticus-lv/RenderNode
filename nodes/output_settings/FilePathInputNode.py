import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeFilePathInputNode(RenderStackNode):
    bl_idname = "RSNodeFilePathInputNode"
    bl_label = "File Path"

    use_blend_file_path: BoolProperty(name="Save at blend file folder", default=True)
    path: StringProperty(default='C:/tmp/')
    path_format: StringProperty(default="$task/$camera", name="Format Name")

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, 'use_blend_file_path')
        if not self.use_blend_file_path:
            row = layout.row(align=1)
            row.prop(self, 'path')
            row.operator('buttons.directory_browse', icon='FILEBROWSER', text='')
        sp = layout.split(factor=0.4)
        sp.label(text="Format Name")
        sp.prop(self, 'path_format',text='')


def register():
    bpy.utils.register_class(RSNodeFilePathInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFilePathInputNode)
