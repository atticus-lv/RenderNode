import bpy
import re
import os
import time

from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector

enum_path_exp = [
    ('', 'File', ''),
    ('$path', 'File Path', ''),
    ('$blend', 'File Name', ''),
    ('', 'Context', ''),
    ('$label', 'Task Label', ''),
    ('$engine', 'Render Engine', ''),
    ('$camera', 'Scene Camera', ''),
    ('$res_x', 'Resolution X', ''),
    ('$res_y', 'Resolution Y', ''),
    ('$ev', 'Exposure Value', ''),
    ('$vl', 'View Layer', ''),
    ('', 'Time', ''),
    ('$T{%m}', 'Date: month', ''),
    ('$T{%d}', 'Date: day', ''),
    ('$T{%H}', 'Time: hour', ''),
    ('$T{%M}', 'Time: minute', ''),
]


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

    if self.operate_type == 'Custom':
        self.create_input('RenderNodeSocketString', 'data_path', 'Data Path(Full)')
    else:
        self.remove_input('data_path')

    if self.operate_type == 'RenderListIndex':
        self.create_output('RenderNodeSocketInt', 'render_list_index', 'Index')
    else:
        self.remove_output('render_list_index')

    self.execute_tree()


class RenderNodeInfoInput(RenderNodeBase):
    bl_idname = 'RenderNodeInfoInput'
    bl_label = 'Information Input'

    operate_type: EnumProperty(name='Type', items=[
        ('PathExp', 'Path Expression', ''),
        ('RenderListIndex', 'Render List Index', ''),
        ('Object', 'Object', ''),
        ('Material', 'Material', ''),
        ('World', 'World', ''),
        ('Collection', 'Collection', ''),
        ('Action', 'Action', ''),
        ('Custom', 'Custom', ''),
    ], default='Object', update=update_node)

    path_exp: EnumProperty(name='Path Exp', items=enum_path_exp, update=update_node, default='$blend')
    render_list_node: StringProperty(name='Render List Node')

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

        elif self.operate_type == 'RenderListIndex':
            layout.prop_search(self, 'render_list_node', context.space_data.node_tree, 'nodes')

    def process(self, context, id, path):
        if self.operate_type == 'PathExp':
            postfix = self.get_postfix(self.path_exp)
            self.outputs['name'].set_value(postfix)

        if self.operate_type == 'RenderListIndex':
            node = context.space_data.node_tree.nodes.get(self.render_list_node)
            cur_task = context.space_data.node_tree.nodes.get(context.window_manager.rsn_viewer_node)

            if node and cur_task:
                if not hasattr(node,'task_list'): return
                for i, task_item in enumerate(node.task_list):
                    if task_item.name == context.window_manager.rsn_viewer_node:
                        self.outputs['render_list_index'].set_value(i)
                        break


        elif self.operate_type == 'Custom':
            dp = self.inputs['data_path'].get_value()
            if dp:
                obj = eval(dp)
                self.outputs['name'].set_value(str(obj))

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

        if path_exp == '$path':
            return bpy.data.filepath

        elif path_exp == '$blend':
            try:
                return bpy.path.basename(bpy.data.filepath)[:-6]
            except Exception:
                return 'unsaved'

        elif path_exp == '$label':
            active_task = self.id_data.nodes.get(bpy.context.window_manager.rsn_viewer_node)
            return active_task.label if active_task else ''

        elif path_exp == '$camera':
            cam = scn.camera
            return cam.name if cam else ''

        elif path_exp == '$engine':
            return scn.render.engine

        elif path_exp == '$res_x':
            return str(scn.render.resolution_x)

        elif path_exp == '$res_y':
            return str(scn.render.resolution_y)

        elif path_exp == '$vl':
            return bpy.context.view_layer.name

        elif path_exp == '$ev':
            return bpy.context.scene.view_settings.exposure

        elif path_exp in {'$T{%m}', '$T{%d}', '$T{%H}', '$T{%M}'}:
            postfix = ''
            TIME = re.findall(r'([$]T{.*?})', path_exp)
            if len(TIME) > 0:
                for i, string in enumerate(TIME):
                    format = time.strftime(TIME[i][3:-1], time.localtime())
                    postfix = postfix.replace(TIME[i], format)
            return postfix


def register():
    bpy.utils.register_class(RenderNodeInfoInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeInfoInput)
