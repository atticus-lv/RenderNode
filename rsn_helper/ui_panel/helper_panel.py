import bpy

class HELPER_PT_Panel(bpy.types.Panel):
    bl_idname = 'HELPER_PT_Panel'
    bl_label = 'RSN Helper'
    bl_category = 'Item'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type ='UI'

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.bl_idname =='RenderStackNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.label(text='Call out helper menu',icon = "EVENT_F")
        # layout.operator("rsn.move_node",text= 'Simple Task',icon = 'ADD')
        # layout.operator("rsn.merge_task",text= 'Merge Task',icon = 'SHORTDISPLAY')


def register():
    bpy.utils.register_class(HELPER_PT_Panel)

def unregister():
    bpy.utils.unregister_class(HELPER_PT_Panel)