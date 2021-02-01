import bpy
from bpy.props import StringProperty


class RSN_OT_SwitchSetting(bpy.types.Operator):
    """Switch between 2 nodes with switch node"""
    bl_idname = 'rsn.switch_setting'
    bl_label = 'Switch'
    bl_options = {'REGISTER', 'UNDO'}

    node: StringProperty(default='')

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and bpy.context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree

        try:
            node = nt.nodes[self.node]
            node1 = node.inputs[0].links[0].from_node
            node2 = node.inputs[1].links[0].from_node

            nt.links.new(node.inputs[1], node1.outputs[0])
            nt.links.new(node.inputs[0], node2.outputs[0])
        except:
            pass

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_SwitchSetting)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SwitchSetting)
