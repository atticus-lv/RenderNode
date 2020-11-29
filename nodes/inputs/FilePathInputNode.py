import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class FilePathInputNode(RenderStackNode):
    bl_idname = "FilePathInputNode"
    bl_label = "File Path"

    use_blend_file_path: BoolProperty(name="Use blend file path", default=True)
    path: StringProperty(default='/tmp/')
    path_format: StringProperty(default="$task/$camera")

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'use_blend_file_path')
        if not self.use_blend_file_path:
            layout.prop(self, 'path')
        layout.prop(self, 'path_format')


def register():
    bpy.utils.register_class(FilePathInputNode)


def unregister():
    bpy.utils.unregister_class(FilePathInputNode)
