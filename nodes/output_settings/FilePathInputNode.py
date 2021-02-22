import bpy
from bpy.props import BoolProperty, StringProperty

from ...nodes.BASE.node_tree import RenderStackNode
from ...preferences import get_pref

import os
import time


def update_node(self, context):
    self.update_parms()


class RSNodeFilePathInputNode(RenderStackNode):
    bl_idname = "RSNodeFilePathInputNode"
    bl_label = "File Path"

    use_blend_file_path: BoolProperty(name="Save in file folder",
                                      description='Save in blend file folder',
                                      default=True, update=update_node)

    custom_path: StringProperty(name='Path',
                                default='', update=update_node)

    path_format: StringProperty(default="$blend_render/$label$camera",
                                name="Formatted Name",
                                description='Formatted Name,View sidebar usage',
                                update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.path_format = get_pref().node_file_path.path_format
        self.width = 250

    def draw_buttons(self, context, layout):
        if bpy.data.filepath == '':
            layout.label(text='Save your file first', icon='ERROR')
        else:
            # custom path
            layout.prop(self, 'use_blend_file_path')
            if not self.use_blend_file_path:
                row = layout.row(align=1)
                row.prop(self, 'custom_path')
                row.operator('buttons.directory_browse', icon='FILEBROWSER', text='')
            # format_name
            row = layout.row(align=1)
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

    def get_data(self):
        task_data = {}
        # get the save location of the images
        if self.use_blend_file_path:
            task_data['path'] = os.path.dirname(bpy.data.filepath) + "/"
        else:
            task_data['path'] = self.custom_path
        # path expression
        task_data['path_format'] = self.path_format

        return task_data


class RSN_OT_AddFormatName(bpy.types.Operator):
    bl_idname = "rsn.add_format_name"
    bl_label = "Add Format Name"
    bl_options = {'REGISTER', 'UNDO'}

    format_name: StringProperty(default='')

    def execute(self, context):
        try:
            node = context.space_data.edit_tree.nodes.active
            if hasattr(node, 'path_format'):
                node.path_format += self.format_name
        except:
            pass

        return {"FINISHED"}


format_names = {
    'File Name'          : '$blend',
    'Task Label'         : '$label',
    'Render Engine'      : '$engine',
    'Camera Name'        : '$camera',
    'Resolution: XxY'    : '$res',
    'Exposure Value'     : '$ev',
    'View Layer'         : '$vl',
    'Date: month-day'    : '$data',
    'Time: minute-second': '$time',
}


class RSN_MT_FormatNameMenu(bpy.types.Menu):
    bl_label = "FormatName Selector"

    def draw(self, context):
        layout = self.layout

        for k, v in format_names.items():
            layout.operator("rsn.add_format_name", text=k).format_name = v

        layout.separator()
        layout.operator("rsn.add_format_name", text="Creat Folder",
                        icon="NEWFOLDER").format_name = '/'


def register():
    bpy.utils.register_class(RSNodeFilePathInputNode)
    bpy.utils.register_class(RSN_OT_AddFormatName)
    bpy.utils.register_class(RSN_MT_FormatNameMenu)


def unregister():
    bpy.utils.unregister_class(RSNodeFilePathInputNode)
    bpy.utils.unregister_class(RSN_OT_AddFormatName)
    bpy.utils.unregister_class(RSN_MT_FormatNameMenu)
