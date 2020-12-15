import bpy


class RSN_OT_MuteNodes(bpy.types.Operator):
    bl_idname = "rsn.mute_nodes"
    bl_label = "Mute Nodes"

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nodes = context.selected_nodes
        if len(nodes) > 0 and nodes[0].mute is False:
            for node in nodes:
                if node.type != "rsn.mute_nodes": node.mute = 1

        elif len(nodes) > 0 and nodes[0].mute is True:
            for node in nodes:
                if node.type != "rsn.mute_nodes": node.mute = 0

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_MuteNodes)


def unregister():
    bpy.utils.unregister_class(RSN_OT_MuteNodes)
