import bpy
from bpy.props import StringProperty


class RSN_OT_MuteNodes(bpy.types.Operator):
    bl_idname = "rsn.mute_nodes"
    bl_label = "Mute Nodes"

    node_name: StringProperty(default='')

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderNodeTree'

    def execute(self, context):
        if self.node_name == '':
            nodes = context.selected_nodes
            for node in nodes:
                node.mute = 0 if node.mute else 1

        else:
            node = bpy.context.space_data.edit_tree.nodes[self.node_name]
            node.mute = 0 if node.mute else 1

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_MuteNodes)


def unregister():
    bpy.utils.unregister_class(RSN_OT_MuteNodes)
