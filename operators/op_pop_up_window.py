import bpy
from bpy.props import BoolProperty, StringProperty, IntProperty


class RSN_OT_SwitchToBindTree(bpy.types.Operator):
    """Need to set one area to Render Editor"""
    bl_idname = 'rsn.switch_to_bind_tree'
    bl_label = 'Find Bind Tree'

    pop: BoolProperty(default=False, description='Pop a new window')

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'NODE_EDITOR':
                area.spaces[0].node_tree = context.scene.rsn_bind_tree
                break

        return {'FINISHED'}


class RSN_OT_PoPEditor(bpy.types.Operator):
    """Popup shader editor window"""
    bl_idname = "rsn.pop_editor"
    bl_label = "Pop Editor"

    bind_tree: BoolProperty(default=False)

    area_type: StringProperty(default='PROPERTIES')
    wd_width: IntProperty(default=1080)
    wd_height: IntProperty(default=720)

    def execute(self, context):
        # set display type
        self.ori_render_display_type = context.preferences.view.render_display_type
        context.preferences.view.render_display_type = "WINDOW"
        # Modify Scene settings
        window = context.scene.render

        ORx = window.resolution_x
        ORy = window.resolution_y
        Oscale = window.resolution_percentage

        window.resolution_x = self.wd_width
        window.resolution_y = self.wd_height
        window.resolution_percentage = 100

        bpy.ops.render.view_show("INVOKE_DEFAULT")
        bpy.context.window_manager.windows[-1].screen.areas[0].type = self.area_type

        bpy.context.space_data.show_region_ui = False

        # bind_tree
        if self.bind_tree:
            context.space_data.node_tree = context.scene.rsn_bind_tree

        # restore
        window.resolution_x = ORx
        window.resolution_y = ORy
        window.resolution_percentage = Oscale
        context.preferences.view.render_display_type = self.ori_render_display_type

        # self.report({'INFO'}, "Material show！")
        # self.finish()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SwitchToBindTree)
    bpy.utils.register_class(RSN_OT_PoPEditor)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SwitchToBindTree)
    bpy.utils.unregister_class(RSN_OT_PoPEditor)
