import bpy
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.update_parms()


class WorkBenchRenderSettingsNode(RenderNodeBase):
    '''A simple input node'''
    bl_idname = 'RSNodeWorkBenchRenderSettingsNode'
    bl_label = 'WorkBench Settings'

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        pass
        # shading = context.Scene.display.shading
        # col = layout.column()
        # split = col.split(factor=0.9)
        #
        # col = split.column()
        # sub = col.row()
        # sub.scale_y = 0.6
        # sub.template_icon_view(shading, "studio_light", scale_popup=3)
        #
        # col = split.column()
        # col.operator("preferences.studiolight_show", emboss=False, text="", icon='PREFERENCES')
        #
        # split = layout.split(factor=0.9)
        # col = split.column()
        # col.prop(shading, "studiolight_rotate_z", text="Rotation")
        # col.prop(shading, "studiolight_intensity")
        # col.prop(shading, "studiolight_background_alpha")
        # col.prop(shading, "studiolight_background_blur")
        # col = split.column()  # to align properly with above

    def get_data(self):
        task_data = {}
        task_data['engine'] = 'BLENDER_WORKBENCH'
        return task_data


def register():
    bpy.utils.register_class(WorkBenchRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(WorkBenchRenderSettingsNode)
