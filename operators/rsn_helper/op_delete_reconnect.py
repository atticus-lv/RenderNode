import bpy
from bpy.props import StringProperty
from ...preferences import get_pref


class RSN_OT_delete_reconnect(bpy.types.Operator):
    """Select the object as the active object"""
    bl_idname = 'rsn.delete_reconnect'
    bl_label = 'Delete Reconnect'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.space_data and hasattr(context.space_data, 'node_tree'):
            return context.area.ui_type == 'RenderNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree
        active_node = nt.nodes.active

        if len(active_node.outputs) == 0:
            nt.nodes.remove(active_node)
            return {"FINISHED"}

        tg_output = None
        tg_input = None

        for output in active_node.outputs:
            if output.is_linked: tg_output = output
            break

        if tg_output is None:
            nt.nodes.remove(active_node)
            return {"FINISHED"}

        for input in active_node.inputs:
            if input.is_linked and input.bl_idname == tg_output.bl_idname:
                tg_input = input
                break

        if tg_input is None:
            for input in active_node.inputs:
                if input.is_linked:
                    tg_input = input
                break

        if tg_input is None:
            nt.nodes.remove(active_node)
            return {"FINISHED"}

        for link in tg_output.links:
            socket = link.to_socket
            nt.links.new(tg_input.links[0].from_socket, socket)

        nt.nodes.remove(active_node)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_delete_reconnect)


def unregister():
    bpy.utils.unregister_class(RSN_OT_delete_reconnect)
