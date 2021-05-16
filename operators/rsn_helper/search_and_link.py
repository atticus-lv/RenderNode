import bpy
import nodeitems_utils
from bpy.props import EnumProperty, IntProperty, StringProperty

from ...preferences import get_pref


class RSN_OT_SearchAndLink(bpy.types.Operator):
    bl_idname = "rsn.search_and_link"
    bl_label = "Search Add"
    bl_property = "node_item"
    bl_options = {"REGISTER", "UNDO"}

    nt = None
    node_name: StringProperty()
    input_id: IntProperty()
    output_id: IntProperty()

    _enum_item_hack = []  # hack method from node_tabber

    def execute(self, context):
        new_node = context.space_data.edit_tree.nodes.new(type=self.node_item)

        # get the socket type is input/output
        # define in socket_type.py, 666 is just a number that much larger than the number of inputs
        try:
            if self.input_id != 666:
                context.space_data.edit_tree.links.new(
                    context.space_data.edit_tree.nodes[self.node_name].inputs[self.input_id],
                    new_node.outputs[0])

            elif self.output_id != 666:
                context.space_data.edit_tree.links.new(
                    context.space_data.edit_tree.nodes[self.node_name].outputs[self.output_id],
                    new_node.inputs[0])

        except Exception as e:
            print(e)

        # get the location for the new node
        context.space_data.edit_tree.active = new_node
        new_node.location = context.space_data.cursor_location[0] - new_node.width / 2, \
                            context.space_data.cursor_location[1]
        bpy.ops.node.select_all(action='DESELECT')
        new_node.select = 1
        # quick place
        if not get_pref().quick_place:
            bpy.ops.transform.translate('INVOKE_DEFAULT')

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'FINISHED'}

    def node_enum_items(self, context):
        enum_items = RSN_OT_SearchAndLink._enum_item_hack
        enum_items.clear()

        for index, item in enumerate(nodeitems_utils.node_items_iter(context)):
            if isinstance(item, nodeitems_utils.NodeItem):
                enum_items.append(
                    (item.nodetype, item.label, ''))

        return enum_items

    populate = node_enum_items

    node_item: EnumProperty(
        name="Node Type",
        description="Node type",
        items=populate,
    )


def register():
    bpy.utils.register_class(RSN_OT_SearchAndLink)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SearchAndLink)
