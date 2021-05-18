import bpy
from bpy.props import *

from ...nodes.BASE.node_tree import RenderStackNode
from ...preferences import get_pref

import os
import time
import re


def update_node(self, context):
    self.update_parms()


class RenderNodeSceneFilePath(RenderStackNode):
    bl_idname = "RenderNodeSceneFilePath"
    bl_label = "Scene File Path"

    save_rel_folder: BoolProperty(name="Save to Relative",
                                  description='Save Image to Relative Folder(locate at .blend)',
                                  default=True, update=update_node)

    custom_path: StringProperty(name='Path',
                                default='', update=update_node)

    version: IntProperty(name='Version', default=1, min=1, soft_max=5, update=update_node)

    def init(self, context):
        self.create_prop('RenderNodeSocketInt', 'version', 'Version')
        self.create_prop('RenderNodeSocketString', 'path_expression', 'Path Exp')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.inputs['path_expression'].value = get_pref().node_file_path.path_format

        self.width = 250

    def draw_buttons(self, context, layout):
        if bpy.data.filepath == '':
            layout.scale_y = 1.25
            layout.label(text='Save your file first', icon='ERROR')
        else:
            # custom path
            layout.prop(self, 'save_rel_folder')
            if not self.save_rel_folder:
                row = layout.row(align=1)
                row.prop(self, 'custom_path')
                row.operator('buttons.directory_browse', icon='FILEBROWSER', text='')

            # viewer node tips
            pref = get_pref()
            if not pref.node_task.update_path:
                layout.label(text='Update is disable in task node', icon='ERROR')

    def process(self):
        self.store_data()
        directory_path = self.make_path()
        if not directory_path: return None

        postfix = self.get_postfix()

        path = os.path.join(directory_path, postfix)
        bpy.context.scene.render.filepath = path

    def make_path(self):
        """only save files will work"""

        if self.save_rel_folder:
            directory_path = bpy.path.abspath('//')
        else:
            if self.custom_path == '': return '//unSaveFile'
            directory_path = os.path.dirname(self.custom_path)
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            return directory_path
        except Exception as e:
            print(e)
            return None

    def get_postfix(self):
        """path expression"""
        scn = bpy.context.scene
        cam = scn.camera
        active_task = bpy.context.space_data.node_tree.nodes.get(bpy.context.window_manager.rsn_viewer_node)

        blend_name = ''

        postfix = self.node_dict["path_expression"]
        # replace camera name
        if cam:
            postfix = postfix.replace('$camera', cam.name)
        else:
            postfix = postfix
        # replace engine
        postfix = postfix.replace('$engine', bpy.context.scene.render.engine)
        # replace res
        postfix = postfix.replace('$res', f"{scn.render.resolution_x}x{scn.render.resolution_y}")
        # replace label
        postfix = postfix.replace('$label', active_task.label)
        # replace view_layer
        postfix = postfix.replace('$vl', bpy.context.view_layer.name)
        # version_
        postfix = postfix.replace('$V', str(self.node_dict["version"]))

        # frame completion
        STYLE = re.findall(r'([$]F\d)', postfix)
        if len(STYLE) > 0:
            c_frame = bpy.context.scene.frame_current
            for i, string in enumerate(STYLE):
                format = f'0{STYLE[i][-1:]}d'
                postfix = postfix.replace(STYLE[i], f'{c_frame:{format}}')

        # time format
        TIME = re.findall(r'([$]T{.*?})', postfix)
        if len(TIME) > 0:
            for i, string in enumerate(TIME):
                format = time.strftime(TIME[i][3:-1], time.localtime())
                postfix = postfix.replace(TIME[i], format)

        # replace filename
        try:
            blend_name = bpy.path.basename(bpy.data.filepath)[:-6]
            postfix = postfix.replace('$blend', blend_name)
        except Exception:
            return 'untitled'

        return postfix


format_names = {
    'File Name': '$blend',
    'Version': '$V',
    'Task Label': '$label',
    'Render Engine': '$engine',
    'Camera Name': '$camera',
    'Resolution: XxY': '$res',
    'Exposure Value': '$ev',
    'View Layer': '$vl',
    'Date: month-day': '$T{%m-%d}',
    'Time: Hour-Minute': '$T{%H-%M}',
}


def register():
    bpy.utils.register_class(RenderNodeSceneFilePath)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneFilePath)
