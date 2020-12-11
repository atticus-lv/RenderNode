import bpy

class HELPER_PT_Panel(bpy.types.Panel):
    bl_idname = 'HELPER_PT_Panel'
    bl_label = 'RSN Helper'
    bl_category = 'RSN'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type ='UI'

    @classmethod
    def poll(self, context):
        return bpy.context.space_data.edit_tree.bl_idname =='RenderStackNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.operator("rsn.simple_task")


def register():
    bpy.utils.register_class(HELPER_PT_Panel)

def unregister():
    bpy.utils.unregister_class(HELPER_PT_Panel)