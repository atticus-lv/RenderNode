import bpy
import numpy
from bpy.props import IntProperty

class RSN_OT_MergeSelectedNodes(bpy.types.Operator):
    bl_idname = 'rsn.merge_selected_nodes'
    bl_label = 'Merge Selection'

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree

        tasks = [{'node': node, 'loc_y': int(node.location[1])} for node in context.selected_nodes if
                 node.bl_idname in {'RSNodeTaskNode','RSNodeSettingsMergeNode'}]

        nodes = [{'node': node, 'loc_y': int(node.location[1])} for node in context.selected_nodes if
                 node.bl_idname not in {'RSNodeTaskNode', 'RSNodeProcessorNode', 'RSNodeRenderListNode',
                                        'RSNodeTaskListNode', 'NodeReroute'}]

        tasks = [dict['node'] for dict in sorted(tasks, key=lambda k: k['loc_y'], reverse=True)]
        nodes = [dict['node'] for dict in sorted(nodes, key=lambda k: k['loc_y'], reverse=True)]

        if len(nodes) == 0 and len(tasks) == 0:
            return {"FINISHED"}

        if len(nodes) > len(tasks):
            need_to_sort = nodes
        else:
            need_to_sort = tasks

        list_node = nt.nodes.new('RSNodeSettingsMergeNode')
        loc_x = numpy.mean([node.location[0] for node in need_to_sort])
        loc_y = numpy.mean([node.location[1] for node in need_to_sort])
        list_node.location = loc_x + 200, loc_y

        for i, node in enumerate(need_to_sort):
            if i < 2:
                nt.links.new(node.outputs[0], list_node.inputs[i])
            else:
                list_node.inputs.new('RSNodeSocketTaskSettings', "Input")
                nt.links.new(node.outputs[0], list_node.inputs[i])

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_MergeSelectedNodes)


def unregister():
    bpy.utils.unregister_class(RSN_OT_MergeSelectedNodes)
