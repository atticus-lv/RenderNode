import bpy
from bpy.props import *


class RSNode_OT_EditInput(bpy.types.Operator):
    """Add/Remove socket input for active node
    """
    bl_idname = "rsnode.edit_input"
    bl_label = "Add Task"

    remove: BoolProperty(name="remove action", default=False)
    socket_type: StringProperty(default='NodeSocketColor')
    socket_name: StringProperty(default="Input")

    def execute(self, context):
        node_tree = bpy.context.space_data.edit_tree
        active_node = node_tree.nodes.active
        if not self.remove:
            active_node.inputs.new(self.socket_type, self.socket_name)
        else:
            for input in active_node.inputs:
                if not input.is_linked:
                    active_node.inputs.remove(input)

        return {"FINISHED"}





def register():
    bpy.utils.register_class(RSNode_OT_EditInput)


def unregister():
    bpy.utils.unregister_class(RSNode_OT_EditInput)
