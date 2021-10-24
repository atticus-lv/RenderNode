import bpy
from bpy.props import StringProperty


class RSN_OT_SelectObject(bpy.types.Operator):
    """Select the object as the active object"""
    bl_idname = 'rsn.select_object'
    bl_label = 'Select'
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty(default='')

    @classmethod
    def poll(self, context):
        if hasattr(context.space_data,'edit_tree'):
            return context.space_data.edit_tree and bpy.context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        if self.name:
            ob = bpy.data.objects[self.name]
            ob.select_set(True)
            context.view_layer.objects.active = ob

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_SelectObject)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SelectObject)
