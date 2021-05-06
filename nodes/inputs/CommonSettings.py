import bpy
import os
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode, get_pref


def poll_camera(self, object):
    return object.type == 'CAMERA'


def update_node(self, context):
    self.update_parms()


class RSNodeCommonSettingsNode(RenderStackNode):
    """A simple Task node"""
    bl_idname = "RSNodeCommonSettingsNode"
    bl_label = 'Common Settings'

    show_filepath: BoolProperty(default=False, name='File Path')
    show_fileformat: BoolProperty(default=False, name='File Format')
    show_dimensions: BoolProperty(default=False, name='Demensions')
    # CAMERA
    ##############################
    camera: PointerProperty(name="Camera", type=bpy.types.Object, poll=poll_camera, update=update_node)

    # RENDER SETTINGS
    ##############################
    engine: EnumProperty(name='Engine', items=[('BLENDER_EEVEE', 'Eevee', ''),
                                               ('BLENDER_WORKBENCH', 'WorkBench', ''),
                                               ('CYCLES', 'Cycles', '')],
                         default='BLENDER_EEVEE', update=update_node)

    # FILEPATH
    ##############################
    use_blend_file_path: BoolProperty(name="Save in file folder",
                                      description='Save in blend file folder',
                                      default=True, update=update_node)

    custom_path: StringProperty(name='Path',
                                default='', update=update_node)

    path_format: StringProperty(default="$blend_render/$V/$label.$camera.$F4",
                                name="Formatted Name",
                                description='Formatted Name,View sidebar usage',
                                update=update_node)

    version: IntProperty(name='Version', default=1, min=1, soft_max=5, update=update_node)

    # FILE FORMAT
    ##############################
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
    quality: IntProperty(name='Quality', default=90, min=0, max=100, subtype='PERCENTAGE')
    # png file
    compression: IntProperty(name="Compression", default=15, min=0, max=100, subtype='PERCENTAGE')
    transparent: BoolProperty(default=False, name="Transparent", update=update_node)

    # demensions
    ##############################
    resolution_x: IntProperty(name="Resolution X", default=1920, min=4, subtype='PIXEL', update=update_node)
    resolution_y: IntProperty(name="Resolution Y", default=1080, min=4, subtype='PIXEL', update=update_node)
    resolution_percentage: IntProperty(name="%", default=100, min=1, subtype='PERCENTAGE', soft_min=1, soft_max=100,
                                       update=update_node)

    frame_start: IntProperty(name="Frame Start", default=1, min=0, update=update_node)
    frame_end: IntProperty(name="Frame End", default=1, min=0, update=update_node)
    frame_step: IntProperty(name="Frame Step", default=1, min=1, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.label = self.name
        self.width = 220

    def draw_buttons(self, context, layout):
        box = layout.column(align=1).split().box()
        box.prop(self, 'camera')

        box = layout.column(align=1).split().box()
        box.prop(self, 'engine')

        #########################
        box = layout.column(align=1).split().box()
        col = box.column(align=1)
        col.prop(self, 'show_filepath', emboss=0, toggle=1, icon='TRIA_DOWN' if self.show_filepath else 'TRIA_RIGHT')
        col.separator(factor=0.5)
        if self.show_filepath:
            if bpy.data.filepath == '':
                col.label(text='Save your file first', icon='ERROR')
            else:
                # custom path
                col.prop(self, 'use_blend_file_path')
                if not self.use_blend_file_path:
                    row = col.row(align=1)
                    row.prop(self, 'custom_path')
                    row.operator('buttons.directory_browse', icon='FILEBROWSER', text='')

                col.prop(self, "version", slider=1)

                # format_name
                row = col.row(align=1)
                row.prop(self, 'path_format', text='')
                # format_name selector
                try:
                    if hasattr(bpy.context.space_data, 'edit_tree'):
                        if bpy.context.space_data.edit_tree.nodes.active.name == self.name:
                            row.menu(menu='RSN_MT_FormatNameMenu', text='', icon='EYEDROPPER')
                except Exception:
                    pass
                # viewer node tips
                pref = get_pref()
                if not pref.node_viewer.update_path:
                    layout.label(text='Update is disable in viewer node', icon='ERROR')

        #########################
        box = layout.column(align=1).split().box()
        col = box.column(align=1)
        col.prop(self, 'show_fileformat', emboss=0, toggle=1,
                 icon='TRIA_DOWN' if self.show_fileformat else 'TRIA_RIGHT')
        col.separator(factor=0.5)
        if self.show_fileformat:
            col.prop(self, 'file_format')
            col.prop(self, 'color_mode')
            col.prop(self, 'color_depth')

            if self.file_format in {'OPEN_EXR_MULTILAYER', 'OPEN_EXR'}:
                col.prop(self, 'use_preview')
            if self.file_format == "PNG":
                col.prop(self, 'compression', slider=1)
            if self.file_format == "JPEG":
                col.prop(self, 'quality', slider=1)
            col.prop(self, 'transparent')

        ##########################
        box = layout.column(align=1).split().box()
        col = box.column(align=1)

        col.prop(self, 'show_dimensions', emboss=0, toggle=1,
                 icon='TRIA_DOWN' if self.show_dimensions else 'TRIA_RIGHT')
        col.separator(factor=0.5)

        if self.show_dimensions:
            row = col.row(align=1)
            row.prop(self, 'resolution_x')
            row.prop(self, 'resolution_y')
            col.prop(self, 'resolution_percentage', )

            col.separator(factor=0.5)

            row = col.row(align=1)
            row.prop(self, 'frame_start', text='Start')
            row.prop(self, 'frame_end', text='End')
            col.prop(self, 'frame_step')

    def get_data(self):
        task_data = {}
        if self.camera: task_data["camera"] = f"bpy.data.objects['{self.camera.name}']"

        task_data['engine'] = self.engine

        ##########################
        # get the save location of the images
        if self.use_blend_file_path:
            task_data['path'] = os.path.dirname(bpy.data.filepath) + "/"
        else:
            if self.custom_path == '':
                task_data['path'] = os.path.dirname(bpy.data.filepath) + "/"
            else:
                task_data['path'] = self.custom_path
        # path expression
        task_data['path_format'] = self.path_format
        task_data['version'] = str(self.version)

        ##########################
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

        ##########################
        if self.frame_end < self.frame_start:
            self.frame_end = self.frame_start
        task_data["frame_start"] = self.frame_start
        task_data["frame_end"] = self.frame_end
        task_data["frame_step"] = self.frame_step

        task_data["res_x"] = self.resolution_x
        task_data['res_y'] = self.resolution_y
        task_data['res_scale'] = self.resolution_percentage

        return task_data


def register():
    bpy.utils.register_class(RSNodeCommonSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCommonSettingsNode)
