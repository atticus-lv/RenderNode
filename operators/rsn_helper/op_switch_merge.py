import bpy
from bpy.props import StringProperty

import numpy


class RSN_OT_switch_merge(bpy.types.Operator):
    """Switch between 2 nodes with switch node"""
    bl_idname = 'rsn.switch_setting'
    bl_label = 'Switch Merge'
    bl_options = {'REGISTER', 'UNDO'}

    node: StringProperty(default='')

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and bpy.context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree
        selected_nodes = [i for i in nt.nodes if i.select]
        if len(selected_nodes) == 0: return {'CANCELLED'}

        nodes = [{'node': node, 'loc_y': int(node.location[1])} for node in context.selected_nodes]
        nodes = [dict['node'] for dict in sorted(nodes, key=lambda k: k['loc_y'], reverse=True)]

        loc_x = numpy.mean([node.location[0] for node in nodes])
        loc_y = numpy.mean([node.location[1] for node in nodes])
        width = numpy.mean([node.width for node in nodes])

        node_socket = nodes[0].outputs[0].bl_idname.removeprefix('RenderNodeSocket')

        switch_node = nt.nodes.new(type='RenderNodeSwitch')
        switch_node.operate_type = node_socket
        switch_node.count = len(nodes)
        switch_node.location = loc_x + width * 1.5, loc_y

        for i, node in enumerate(nodes):
            nt.links.new(node.outputs[0], switch_node.inputs[i + 1])

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_switch_merge)


def unregister():
    bpy.utils.unregister_class(RSN_OT_switch_merge)
