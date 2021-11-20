import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

from ...preferences import get_pref

import os
import time
import re


class RenderNodeSetFilePath(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetFilePath'
    bl_label = 'Set Scene File Path'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketFilePath', 'base_path', 'Path', default_value='//')
        self.create_input('RenderNodeSocketInt', 'version', 'Version')
        self.create_input('RenderNodeSocketString', 'path_expression', 'Postfix')
        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.inputs['path_expression'].default_value = get_pref().node_file_path.path_format

        self.width = 200

    def draw_buttons(self, context, layout):
        if bpy.data.filepath == '':
            layout.scale_y = 1.25
            layout.label(text='Save your file first', icon='ERROR')

    def process(self, context, id, path):
        if not self.process_task(): return

        directory_path = self.make_path()
        if not directory_path: return None
        path_exp = self.inputs['path_expression'].get_value()
        v = self.inputs['version'].get_value()
        if path_exp and v is not None:
            postfix = self.get_postfix(path_exp, v)
            rel_path = os.path.join(bpy.path.relpath(directory_path), postfix) if postfix != '' else bpy.path.relpath(
                directory_path) + '/'
            # abs_path = os.path.join(directory_path, postfix) if postfix != '' else directory_path + '/'
            self.task_dict_append({'filepath': rel_path})

    def make_path(self):
        """only save files will work"""
        try:
            path = self.inputs['base_path'].get_value()
            abs_path = bpy.path.abspath(path)
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            return abs_path
        except Exception as e:
            print(e)
            return None

    def get_postfix(self, path_exp, version):
        """path expression"""
        if path_exp == '': return ''

        scn = bpy.context.scene
        cam = scn.camera
        blend_name = ''

        postfix = path_exp
        # replace camera name
        if cam:
            postfix = postfix.replace('$camera', cam.name)
        else:
            postfix = postfix
        # replace engine
        postfix = postfix.replace('$engine', bpy.context.scene.render.engine)
        # replace res
        postfix = postfix.replace('$res', f"{scn.render.resolution_x}x{scn.render.resolution_y}")
        # replace view_layer
        postfix = postfix.replace('$vl', bpy.context.view_layer.name)
        # version_
        postfix = postfix.replace('$V', str(version))

        # frame completion
        STYLE = re.findall(r'([$]F\d)', postfix)
        if len(STYLE) > 0:
            c_frame = bpy.context.scene.frame_current
            for i, string in enumerate(STYLE):
                format = f'0{STYLE[i][-1:]}d'
                frame = f'{c_frame:{format}}' if not bpy.context.window_manager.rsn_running_modal else '#' * int(
                    STYLE[i][-1:])
                postfix = postfix.replace(STYLE[i], frame)

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


def register():
    bpy.utils.register_class(RenderNodeSetFilePath)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetFilePath)
