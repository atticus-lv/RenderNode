import bpy
from bpy.props import BoolProperty,StringProperty
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


    def draw_buttons_ext(self, context, layout):
        box = layout.box()
        col = box.column(align=1)
        col.label(text ="USAGE:")
        col.label(text= '$task: $task in Task Node')
        col.label(text= '$camera: name of scene camera')
        col.label(text= '$res: resolution (XxY)')
        col.label(text= '$engine: render engine')
        col.label(text= '$vl: name of scene view layer')
        col.label(text= '$date: month-day')
        col.label(text= '$time: hour-min')
        col.label(text= '/: create folder,should be a folder name in front of "/"')


def register():
    bpy.utils.register_class(RSNodeFilePathInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFilePathInputNode)
