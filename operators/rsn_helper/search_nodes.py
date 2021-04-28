import bpy
import nodeitems_utils
from bpy.props import EnumProperty

from ...preferences import get_pref


class RSN_OT_SearchNodes(bpy.types.Operator):
    bl_idname = "rsn.search_nodes"
    bl_label = "Quick Search"
    bl_property = "my_search"

    bl_options = {"REGISTER", "UNDO"}

    # def node_enum_items(self, context):
    #     node_items_list = []
    #     for index, item in enumerate(nodeitems_utils.node_items_iter(context)):
    #         if isinstance(item, nodeitems_utils.NodeItem):
    #             node_items_list.append((item.nodetype, item.label, ''))
    #
    #     print(node_items_list)
    #     return node_items_list
    #
    # def create_node(self, context, node_type=None):
    #     if node_type:
    #         bpy.ops.node.select_all(action='DESELECT')
    #
    #         node = context.space_data.edit_tree.nodes.new(type=node_type)
    #
    #         node.select = True
    #         context.space_data.edit_tree.nodes.active = node
    #         node.location = context.space_data.cursor_location
    #         if not get_pref().quick_place:
    #             bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

    #         node.location = space.cursor_location

    # def invoke(self, context, event):
    #     context.window_manager.invoke_search_popup(self)
    #     return {'RUNNING_MODAL'}

    @classmethod
    def poll(self, context):
        return context.space_data and hasattr(context.space_data, 'edit_tree')

    def execute(self, context):
        try:
            if not get_pref().quick_place:
                bpy.ops.node.add_search('INVOKE_DEFAULT', use_transform=True)
            else:
                bpy.ops.node.add_search('INVOKE_DEFAULT', use_transform=False)
        except RuntimeError:
            self.report({"ERROR"}, "No Node Tree here!")

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SearchNodes)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SearchNodes)
