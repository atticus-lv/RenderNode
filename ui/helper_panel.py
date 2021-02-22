import bpy
from bpy.props import *


class HELPER_PT_Panel(bpy.types.Panel):
    bl_idname = 'HELPER_PT_Panel'
    bl_label = 'RSN Helper'
    bl_category = 'Item'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.25
        layout.label(text='Call out helper menu', icon="EVENT_F")

        layout.label(text=f'Update:{context.window_manager.rsn_tree_time}', icon='MOD_TIME')

        try:
            if hasattr(bpy.context.space_data, 'edit_tree'):
                if bpy.context.space_data.edit_tree.nodes.active.bl_idname == 'RSNodeFilePathInputNode':
                    box = layout.box()
                    col = box.column(align=1)
                    col.label(text="USAGE:")
                    col.label(text='$blend: name of your file (save first!)')
                    col.label(text='$F4: frame format:0001 ("4" can be any number)')
                    col.label(text='$label: Task label')
                    col.label(text='$camera: name of scene camera')
                    col.label(text='$res: resolution (XxY)')
                    col.label(text='$engine: render engine')
                    col.label(text='$vl: name of scene view layer')
                    col.label(text='$date: month-day')
                    col.label(text='$time: hour-min')
                    col.label(text='/: create folder,should be dict_input folder name in front of "/"')
        except Exception:
            pass


def register():
    bpy.types.WindowManager.rsn_tree_time = StringProperty()
    bpy.utils.register_class(HELPER_PT_Panel)


def unregister():
    bpy.utils.unregister_class(HELPER_PT_Panel)
