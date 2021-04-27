import bpy


class RSN_OT_SplitToSelected(bpy.types.Operator):
    """Link the active setting node to selected task"""
    bl_idname = 'rsn.split_to_selected'
    bl_label = 'Split to Selected'

    @classmethod
    def poll(cls, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.nodes.active

    def execute(self, context):
        nt = context.space_data.edit_tree
        src_node = context.space_data.edit_tree.nodes.active

        nodes = [node for node in context.selected_nodes if node != src_node]

        for node in nodes:
            for input in node.inputs:
                if not input.is_linked:
                    nt.links.new(src_node.outputs[0], input)
                    break

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SplitToSelected)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SplitToSelected)
