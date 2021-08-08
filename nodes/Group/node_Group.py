import bpy
from bpy.props import *

import uuid

from ...nodes.BASE.node_base import RenderNodeBase
from ...nodes.BASE._runtime import cache_node_group_outputs


class RSN_OP_CreateGroup(bpy.types.Operator):
    bl_idname = "rsn.create_group"
    bl_label = "Create Group"

    node: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR" and context.space_data.tree_type == 'RenderStackNodeTree'

    def execute(self, context):
        tree = context.space_data.edit_tree
        orig_node = tree.nodes[self.node]

        new_node_tree = bpy.data.node_groups.new("Render Group", "RenderStackNodeTreeGroup")

        orig_node.node_tree_selection = new_node_tree
        loop_input = new_node_tree.nodes.new("NodeGroupInput")
        loop_output = new_node_tree.nodes.new("NodeGroupOutput")
        return {'FINISHED'}


class RenderNodeGroup(bpy.types.NodeCustomGroup, RenderNodeBase):
    bl_idname = 'RenderNodeGroup'
    bl_label = 'Render Node Group'

    # bl_icon = 'NODETREE'

    def nested_tree_filter(self, context):
        """Define which tree we would like to use as nested trees."""
        if context.bl_idname != 'RenderStackNodeGroup':  # It should be our dedicated to this class
            return False
        else:
            # to avoid circular dependencies
            for path_tree in bpy.context.space_data.path:
                if path_tree.node_tree.name == context.name:
                    return False
            return True

    def update_group_tree(self, context):
        self.node_tree = self.node_tree_selection

    # attribute for available sub tree
    node_tree_selection: bpy.props.PointerProperty(type=bpy.types.NodeTree, poll=nested_tree_filter,
                                                   update=update_group_tree)

    def init(self, context):
        super().init(context)

    def draw_label(self):
        if self.node_tree:
            return self.node_tree.name

        return 'Node Group'

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)

        row = layout.row(align=True)
        row.prop(self, "node_tree_selection", text="")
        if self.node_tree:
            layout.prop(self.node_tree, 'name', text='Name')
        else:
            row.operator('rsn.create_group', text='', icon='ADD').node = self.name

    def process_group(self, context, id, path):

        outputs = set()
        path = path + [self.name]
        execute_id = str(uuid.uuid4())

        if self.node_tree not in cache_node_group_outputs:
            cache_node_group_outputs[self.node_tree] = []
            for x in self.node_tree.nodes:
                if x.bl_rna.identifier == 'NodeGroupOutput':
                    cache_node_group_outputs[self.node_tree].append(x)

        for x in cache_node_group_outputs[self.node_tree]:
            self.execute_other(context, execute_id, path, x)
            for socket in x.inputs:
                if socket.identifier not in outputs:
                    try:
                        output = next(y for y in self.outputs if y.identifier == socket.identifier)
                    except StopIteration:
                        continue

                    output.set_value(socket.get_value())

                    if socket.links:
                        outputs.add(socket.identifier)
                elif socket.links:
                    raise ValueError(f'Socket {x}:{socket.name} has already been set by another Group Output Node')
                else:
                    pass


def register():
    bpy.utils.register_class(RSN_OP_CreateGroup)
    bpy.utils.register_class(RenderNodeGroup)


def unregister():
    bpy.utils.unregister_class(RSN_OP_CreateGroup)
    bpy.utils.unregister_class(RenderNodeGroup)
