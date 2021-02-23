import os
import time
import json
import math

from bpy.props import *

from ..utility import *
from ..preferences import get_pref


class RSN_OT_RenderButton(bpy.types.Operator):
    """Need Scene Camera"""
    bl_idname = "rsn.render_button"
    bl_label = "Render"

    # get data from root (from the render_list node)
    render_list_node_name: StringProperty()

    # action after render (from the render_list node)
    open_dir: BoolProperty()
    clean_path: BoolProperty()
    render_display_type: StringProperty()

    # task_data
    rsn_queue = None

    # ui
    display_num: IntProperty(name='Max Display Number', min=1, default=10, soft_max=20)
    page_num: IntProperty(name='Page', min=1, default=1, soft_max=5)

    @classmethod
    def poll(self, context):
        if not context.window_manager.rsn_running_modal:
            return context.scene.camera is not None

    # stop the unnecessary viewport rendering
    def change_shading(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D' and space.shading.type == "RENDERED":
                        space.shading.type = 'SOLID'

    def get_render_data(self):
        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()
        self.nt = rsn_tree.get_wm_node_tree()

        self.rsn_queue = RSN_Queue(nodetree=rsn_tree.get_wm_node_tree(), render_list_node=self.render_list_node_name)

    def draw(self, context):
        layout = self.layout
        box = layout.split().box()
        row = box.row(align=1)

        # sheet style
        col1 = row.column(align=1).box()
        col2 = row.column(align=1).box()
        col3 = row.column(align=1).box()
        col4 = row.column(align=1).box()
        col5 = row.column(align=1).box()
        col6 = row.column(align=1).box()
        col7 = row.column(align=1).box()

        col1.scale_x = 0.5
        col7.scale_x = 0.5

        col1.label(text='Index')
        col2.label(text='Node')
        col3.label(text='Label')
        col4.label(text='Frame Range')
        col5.label(text='File Path')
        col6.label(text='File Name')
        col7.label(text='Info')

        # pages
        layout.use_property_split = 1
        layout.use_property_decorate = 0
        layout.prop(self, 'page_num')
        layout.prop(self, 'display_num')
        layout.separator(factor=0.5)

        pages = math.ceil(self.rsn_queue.get_length() / self.display_num)
        if self.page_num > pages: self.page_num = pages

        start_index = math.floor((self.page_num - 1) * self.display_num)
        end_index = start_index + self.display_num

        # draw task
        for i, task_node in enumerate(self.rsn_queue.task_queue):
            if start_index <= i < end_index:
                # Index
                col1.label(text=f'{i}')
                # node and mute
                node = bpy.context.space_data.edit_tree.nodes[task_node]
                col2.prop(node, 'mute', text=task_node, icon='PANEL_CLOSE' if node.mute else 'CHECKMARK')
                # label
                col3.label(text=self.rsn_queue.task_data_queue[i]['label'])
                # Range
                fs = self.rsn_queue.task_data_queue[i]["frame_start"]
                fe = self.rsn_queue.task_data_queue[i]["frame_end"]
                col4.label(text=f'{fs} → {fe} ({fe - fs + 1})')
                # filepath
                if 'path' in self.rsn_queue.task_data_queue[i]:
                    dir = self.rsn_queue.task_data_queue[i]["path"]
                    show = col5.operator('rsn.show_task_details', icon='VIEWZOOM', text='Show')
                    show.task_data = dir
                    show.width = 500
                else:
                    col5.label(text='Not Defined')
                # file name
                if 'path_format' in self.rsn_queue.task_data_queue[i]:
                    format = self.rsn_queue.task_data_queue[i]["path_format"]
                    show = col6.operator('rsn.show_task_details', icon='VIEWZOOM', text='Show')
                    show.task_data = format
                    show.width = 500
                else:
                    col6.label(text='Not Defined')
                # task_data_list
                d = json.dumps(self.rsn_queue.task_data_queue[i], indent=2, ensure_ascii=False)
                col7.operator('rsn.show_task_details', icon='INFO', text='').task_data = d

    def execute(self, context):
        blend_path = context.blend_data.filepath

        if blend_path == "":
            self.report({"ERROR"}, "Save your file first!")
            return {"FINISHED"}
        elif context.scene.render.image_settings.file_format in {'AVI_JPEG', 'AVI_RAW', 'FFMPEG'}:
            self.report({"ERROR"}, "Not Support Anunimation Format")
            return {"FINISHED"}

        self.change_shading()
        bpy.ops.rsn.render_stack_task(render_list_node_name=self.render_list_node_name,
                                      open_dir=self.open_dir,
                                      clean_path=self.clean_path,
                                      render_display_type=self.render_display_type)

        return {'FINISHED'}

    def invoke(self, context, event):
        self.get_render_data()
        return context.window_manager.invoke_props_dialog(self, width=600)


classes = (
    RSN_OT_RenderButton
)


def register():
    bpy.utils.register_class(RSN_OT_RenderButton)


def unregister():
    bpy.utils.unregister_class(RSN_OT_RenderButton)
