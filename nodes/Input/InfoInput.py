import bpy
import re
import os
import time

from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector

format_names = {
    'File Name': '$blend',
    'Render Engine': '$engine',
    'Scene Camera': '$camera',
    'Resolution: XxY': '$res',
    'Exposure Value': '$ev',
    'View Layer': '$vl',
    'Date: month': '$T{%m}',
    'Date: day': '$T{%d}',
    'Time: hour': '$T{%H}',
    'Time: minute': '$T{%M}',
}

enum_path_exp = [(v, k, '') for k, v in format_names.items()]


def update_node(self, context):
    if self.operate_type == 'Object':
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_output('RenderNodeSocketXYZ', 'location', 'Location')
        self.create_output('RenderNodeSocketXYZ', 'scale', 'Scale')
        self.create_output('RenderNodeSocketEuler', 'rotate', 'Rotate')
    else:
        self.remove_input('object')
        self.remove_output('location')
        self.remove_output('scale')
        self.remove_output('rotate')

    if self.operate_type == 'Material':
        self.create_input('RenderNodeSocketMaterial', 'material', 'Material')
    else:
        self.remove_input('material')

    if self.operate_type == 'World':
        self.create_input('RenderNodeSocketWorld', 'world', 'World')
    else:
        self.remove_input('world')

    if self.operate_type == 'Collection':
        self.create_input('RenderNodeSocketCollection', 'collection', 'Collection')
        self.create_output('RenderNodeSocketInt', 'count', 'Objects Count')
    else:
        self.remove_input('collection')
        self.remove_output('count')

    if self.operate_type == 'Action':
        self.create_input('RenderNodeSocketAction', 'action', 'Action')
        self.create_output('RenderNodeSocketInt', 'frame_start', 'Frame Start')
        self.create_output('RenderNodeSocketInt', 'frame_end', 'Frame End')
    else:
        self.remove_input('action')
        self.remove_output('frame_start')
        self.remove_output('frame_end')

    # if self.operate_type == 'PathExp':
    #     self.create_output('RenderNodeSocketString', 'path_exp', 'Path Expression')
    # else:
    #     self.remove_output('path_exp')

    self.execute_tree()


class RenderNodeInfoInput(RenderNodeBase):
    bl_idname = 'RenderNodeInfoInput'
    bl_label = 'Information Input'

    operate_type: EnumProperty(name='Type', items=[
        ('Object', 'Object', ''),
        ('Material', 'Material', ''),
        ('World', 'World', ''),
        ('Collection', 'Collection', ''),
        ('Action', 'Action', ''),
        ('PathExp', 'Path Expression', ''),
    ], default='Object', update=update_node)

    path_exp: EnumProperty(name='Path Exp', items=enum_path_exp, update=update_node, default='$blend')

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_output('RenderNodeSocketString', 'name', "Name")
        self.create_output('RenderNodeSocketXYZ', 'location', 'Location')
        self.create_output('RenderNodeSocketXYZ', 'scale', 'Scale')
        self.create_output('RenderNodeSocketEuler', 'rotate', 'Rotate')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')
        if self.operate_type == 'PathExp':
            layout.prop(self, 'path_exp', text='Source')

    def process(self, context, id, path):
        if self.operate_type == 'PathExp':
            postfix = self.get_postfix(self.path_exp)
            self.outputs['name'].set_value(postfix)
        else:
            pointer = self.inputs[0].get_value()
            if pointer is None: return

            self.outputs['name'].set_value(pointer.name)

            if self.operate_type == 'Object':
                self.outputs['location'].set_value(pointer.location)
                self.outputs['scale'].set_value(pointer.scale)
                self.outputs['rotate'].set_value(pointer.rotation_euler)
            elif self.operate_type == 'Material':
                return
            elif self.operate_type == 'World':
                return
            elif self.operate_type == 'Collection':
                self.outputs['count'].set_value(len(pointer.objects))

            elif self.operate_type == 'Action':
                self.outputs['frame_start'].set_value(round(pointer.frame_range[0]))
                self.outputs['frame_end'].set_value(round(pointer.frame_range[1]))

    def get_postfix(self, path_exp):
        """path expression"""
        scn = bpy.context.scene
        cam = scn.camera
        active_task = self.id_data.nodes.get(bpy.context.window_manager.rsn_viewer_node)
        if active_task == '' or path_exp == '': return ''
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
    bpy.utils.register_class(RenderNodeInfoInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeInfoInput)
