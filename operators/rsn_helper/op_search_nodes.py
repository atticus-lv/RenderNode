import bpy
import nodeitems_utils
from bpy.props import EnumProperty

from ...preferences import get_pref


class RSN_OT_SearchNodes(bpy.types.Operator):
    bl_idname = "rsn.search_nodes"
    bl_label = "Quick Search"
    # bl_property = "my_search"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(self, context):
        if context.space_data and hasattr(context.space_data, 'node_tree'):
            if get_pref().limited_area:
                return context.area.ui_type == 'RenderNodeTree'
            return True

    def execute(self, context):
        try:
            if not get_pref().quick_place:
                bpy.ops.node.add_search(use_transform=True)
            else:
                bpy.ops.node.add_search(use_transform=False)
        except RuntimeError:
            self.report({"ERROR"}, "No Node Tree here!")

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SearchNodes)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SearchNodes)
