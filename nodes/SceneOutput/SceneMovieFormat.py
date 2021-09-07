import bpy
from bpy.props import *

from ...nodes.BASE.node_base import RenderNodeBase
from .SceneResolution import get_preset_folder

import os


def get_enums_from_prop(obj, prop_name):
    return [(item.identifier, item.name, item.description) for item in obj.bl_rna.properties[prop_name].enum_items]


def get_file_format(movie):
    enum_items = get_enums_from_prop(bpy.context.scene.render.image_settings, 'file_format')
    return enum_items[:-3] if not movie else enum_items[-3:]


def enum_ffmpeg_preset():
    ffmpeg_preset_dir = os.path.join(get_preset_folder(), 'ffmpeg')
    enums = [(file_name, file_name[0:-3], '') for file_name in os.listdir(ffmpeg_preset_dir)]
    return enums


def enum_frame_rate_preset():
    ffmpeg_preset_dir = os.path.join(get_preset_folder(), 'framerate')
    enums = [(file_name, file_name[0:-3], '') for file_name in os.listdir(ffmpeg_preset_dir)]
    return enums


def update_node(self, context):
    if self.use_frame_rate_preset:
        self.remove_input('fps')
        self.remove_input('frame_base')
    else:
        self.create_input('RenderNodeSocketInt', 'fps', 'FPS', default_value=24)
        self.create_input('RenderNodeSocketFloat', 'frame_base', 'Base', default_value=1.00)

    self.execute_tree()


class RenderNodeSceneMovieFormat(RenderNodeBase):
    bl_idname = "RenderNodeSceneMovieFormat"
    bl_label = "Scene Movie Format"

    file_format: EnumProperty(name='File Format',
                              items=[('AVI_JPEG', 'AVI JPEG', 'Output video in AVI JPEG format'),
                                     ('AVI_RAW', 'AVI Raw', 'Output video in AVI Raw format'),
                                     ('FFMPEG', 'FFmpeg Video', 'The most versatile way to output video files')],
                              default='FFMPEG',
                              update=update_node)

    color_mode: EnumProperty(name='Color Mode',
                             items=[('BW', 'BW', ''), ('RGB', 'RGB', '')],
                             default='RGB',
                             update=update_node)

    # jpg / AVI
    quality: IntProperty(name='Quality',
                         default=90, min=0, max=100,
                         update=update_node)

    use_ffmpeg_preset: BoolProperty(name='Use FFMPEG Preset', default=False)
    ffmpeg_preset: EnumProperty(name='FFMPEG Preset', items=[
        ('DVD_(note_colon__this_changes_render_resolution).py', 'DVD_(note_colon__this_changes_render_resolution)', ''),
        ('H264_in_Matroska.py', 'H264_in_Matroska', ''),
        ('H264_in_Matroska_for_scrubbing.py', 'H264_in_Matroska_for_scrubbing', ''),
        ('H264_in_MP4.py', 'H264_in_MP4', ''), ('Ogg_Theora.py', 'Ogg_Theora', ''),
        ('WebM_(VP9+Opus).py', 'WebM_(VP9+Opus)', ''), ('Xvid.py', 'Xvid', '')],
                                default='H264_in_MP4.py',
                                update=update_node)

    use_frame_rate_preset: BoolProperty(name='Use Frame Preset', default=True, update=update_node)
    frame_rate_preset: EnumProperty(name='FFMPEG Preset', items=[
        ('23.98.py', '23.98', ''),
        ('24.py', '24', ''),
        ('29.97.py', '29.97', ''),
        ('30.py', '30', ''),
        ('50.py', '50', ''),
        ('59.94.py', '59.94', ''),
        ('60.py', '60', ''),
        ('120.py', '120', ''),
        ('240.py', '240', ''), ],
                                    default='24.py', update=update_node)

    def init(self, context):
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.use_property_split = 1
        col.use_property_decorate = 0

        col.prop(self, 'file_format', icon='FILE_MOVIE')
        row = col.row(align=1)
        row.prop(self, 'color_mode', expand=1)
        if self.file_format == 'AVI_JPEG':
            col.prop(self, 'quality')
        elif self.file_format == 'FFMPEG':
            col.prop(self, 'use_ffmpeg_preset')
            if self.use_ffmpeg_preset: col.prop(self, 'ffmpeg_preset')

        col.prop(self, 'use_frame_rate_preset')
        if self.use_frame_rate_preset: col.prop(self, 'frame_rate_preset')

    def process(self, context, id, path):
        attr_list = ['file_format','quality', ]

        for attr in attr_list:
            try:
                self.compare(bpy.context.scene.render.image_settings, attr, getattr(self, attr))
            except Exception as e:
                print(e)

        if self.file_format == 'FFMPEG':
            if self.use_ffmpeg_preset:
                ffmpeg_preset_dir = os.path.join(get_preset_folder(), 'ffmpeg')
                bpy.ops.script.python_file_run(filepath=os.path.join(ffmpeg_preset_dir, self.ffmpeg_preset))
            if self.use_frame_rate_preset:
                frame_rate_preset_dir = os.path.join(get_preset_folder(), 'framerate')
                bpy.ops.script.python_file_run(filepath=os.path.join(frame_rate_preset_dir, self.frame_rate_preset))
            else:
                context.scene.render.fps = self.inputs['fps'].get_value()
                context.scene.render.frame_base = self.inputs['frame_base'].get_value()


def register():
    bpy.utils.register_class(RenderNodeSceneMovieFormat)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneMovieFormat)
