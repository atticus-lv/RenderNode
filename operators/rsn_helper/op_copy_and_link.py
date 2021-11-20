import bpy
from bpy.props import StringProperty
from ...preferences import get_pref


class RSN_OT_copy_and_link(bpy.types.Operator):
    """Select the object as the active object"""
    bl_idname = 'rsn.copy_and_link'
    bl_label = 'Copy and Link'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.space_data and hasattr(context.space_data, 'node_tree'):
            if get_pref().limited_area:
                return context.area.ui_type == 'RenderStackNodeTree'
            return True

    def execute(self, context):
        nt = context.space_data.edit_tree
        active_node = nt.nodes.active

        if len(active_node.inputs) == 0:
            bpy.ops.node.duplicate_move('INVOKE_DEFAULT')
            return {"FINISHED"}

        src_input_nodes = []
        for i, input in enumerate(active_node.inputs):
            if not input.is_linked: continue
            src_input_nodes.append({i: input.links[0].from_socket})

        bpy.ops.node.duplicate_move('INVOKE_DEFAULT')

        new_node = nt.nodes.active
        for d in src_input_nodes:
            for index, from_socket in d.items():
                nt.links.new(from_socket, new_node.inputs[index])

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_copy_and_link)


def unregister():
    bpy.utils.unregister_class(RSN_OT_copy_and_link)
