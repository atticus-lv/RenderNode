import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class FilePathInputNode(RenderStackNode):
    bl_idname = "FilePathInputNode"
    bl_label = "File Path"

    use_blend_file_path: BoolProperty(name="Save at blend file folder", default=True)
    path: StringProperty(default='/tmp/')
    path_format: StringProperty(default="$task/$camera", name="Format Name")

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, 'use_blend_file_path')
        # if not self.use_blend_file_path:
            # layout.prop(self, 'path')
        layout.label(text ="Format Name:" )
        layout.prop(self, 'path_format',text='')


def register():
    bpy.utils.register_class(FilePathInputNode)


def unregister():
    bpy.utils.unregister_class(FilePathInputNode)
