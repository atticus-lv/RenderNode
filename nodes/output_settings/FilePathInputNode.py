import bpy
from bpy.props import BoolProperty, StringProperty
from RenderStackNode.node_tree import RenderStackNode


def update_node(self, context):
    self.update()


class RSNodeFilePathInputNode(RenderStackNode):
    bl_idname = "RSNodeFilePathInputNode"
    bl_label = "File Path"

    use_blend_file_path: BoolProperty(name="Save in file directory",
                                      description='Save in blend file directory',
                                      default=True, update=update_node)
    path: StringProperty(default='', update=update_node)
    path_format: StringProperty(default="$label/$camera",
                                name="Formatted Name",
                                description='Formatted Name,View sidebar usage',
                                update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.width = 220

    def draw_buttons(self, context, layout):
        layout.prop(self, 'use_blend_file_path')
        if not self.use_blend_file_path:
            row = layout.row(align=1)
            row.prop(self, 'path')
            row.operator('buttons.directory_browse', icon='FILEBROWSER', text='')
        layout.prop(self, 'path_format', text='')

    def draw_buttons_ext(self, context, layout):
        box = layout.box()
        col = box.column(align=1)
        col.label(text="USAGE:")
        col.label(text='$label: Task label')
        col.label(text='$camera: name of scene camera')
        col.label(text='$res: resolution (XxY)')
        col.label(text='$engine: render engine')
        col.label(text='$vl: name of scene view layer')
        col.label(text='$date: month-day')
        col.label(text='$time: hour-min')
        col.label(text='/: create folder,should be a folder name in front of "/"')


def register():
    bpy.utils.register_class(RSNodeFilePathInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFilePathInputNode)
