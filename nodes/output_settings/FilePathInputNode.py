import bpy
from bpy.props import BoolProperty, StringProperty

from ...nodes.BASE.node_tree import RenderStackNode
from ...preferences import get_pref

def update_node(self, context):
    self.update_parms()


class RSNodeFilePathInputNode(RenderStackNode):
    bl_idname = "RSNodeFilePathInputNode"
    bl_label = "File Path"

    use_blend_file_path: BoolProperty(name="Save in file addon_dir",
                                      description='Save in blend file addon_dir',
                                      default=True, update=update_node)
    path: StringProperty(default='', update=update_node)
    path_format: StringProperty(default="$blend_render/$label$camera",
                                name="Formatted Name",
                                description='Formatted Name,View sidebar usage',
                                update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.path_format = get_pref().node_file_path.path_format
        self.width = 220

    def draw_buttons(self, context, layout):
        layout.prop(self, 'use_blend_file_path')
        if not self.use_blend_file_path:
            row = layout.row(align=1)
            row.prop(self, 'path')
            row.operator('buttons.directory_browse', icon='FILEBROWSER', text='')
        layout.prop(self, 'path_format', text='')

        pref = get_pref()
        if not pref.node_viewer.update_path:
            layout.label(text='Update is disable in viewer node',icon = 'ERROR')

def register():
    bpy.utils.register_class(RSNodeFilePathInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFilePathInputNode)
