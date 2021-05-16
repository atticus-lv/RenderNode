import bpy
from bpy.props import BoolProperty,StringProperty,IntProperty


class RSN_OT_PoPEditor(bpy.types.Operator):
    """Popup shader editor window"""
    bl_idname = "rsn.pop_editor"
    bl_label = "Pop Editor"

    area_type: StringProperty(default='PROPERTIES')
    wd_width: IntProperty(default=400)
    wd_height: IntProperty(default=400)

    def execute(self, context):
        # Modify scene settings
        window = context.scene.render

        ORx = window.resolution_x
        ORy = window.resolution_y
        Oscale = window.resolution_percentage

        window.resolution_x = self.wd_width
        window.resolution_y = self.wd_height
        window.resolution_percentage = 100

        bpy.ops.render.view_show("INVOKE_DEFAULT")
        bpy.context.window_manager.windows[-1].screen.areas[0].type = self.area_type

        # restore
        window.resolution_x = ORx
        window.resolution_y = ORy
        window.resolution_percentage = Oscale

        # self.report({'INFO'}, "Material show！")
        # self.finish()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_PoPEditor)


def unregister():
    bpy.utils.unregister_class(RSN_OT_PoPEditor)
