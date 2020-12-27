import bpy
import numpy
from bpy.props import IntProperty


class RSN_OT_MergeTask(bpy.types.Operator):
    bl_idname = 'rsn.merge_task'
    bl_label = 'Merge Task to list'

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree
        # get and sort task node
        tasks = [{'node': node, 'loc_y': int(node.location[1])} for node in context.selected_nodes if
                 node.select and node.bl_idname in {'RSNodeTaskNode'}]
        tasks = [dict['node'] for dict in sorted(tasks, key=lambda k: k['loc_y'], reverse=True)]
        if len(tasks) == 0:
            return {"FINISHED"}

        list_node = nt.nodes.new('RSNodeTaskListNode')
        loc_x = numpy.mean([node.location[0] for node in tasks])
        loc_y = numpy.mean([node.location[1] for node in tasks])
        list_node.location = loc_x + 200, loc_y

        for i, task in enumerate(tasks):
            if i < 3:
                nt.links.new(task.outputs[0], list_node.inputs[i])
            else:
                list_node.inputs.new('RSNodeSocketRenderList', "Task")
                nt.links.new(task.outputs[0], list_node.inputs[i])

        return {"FINISHED"}


class RSN_OT_MergeSettings(bpy.types.Operator):
    bl_idname = 'rsn.merge_settings'
    bl_label = 'Merge Settings'

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree
        nodes = [{'node': node, 'loc_y': int(node.location[1])} for node in context.selected_nodes if
                 node.select and node.bl_idname not in {'RSNodeTaskNode','RSNodeProcessorNode','RSNodeRenderListNode','RSNodeTaskListNode','NodeReroute'}]
        nodes = [dict['node'] for dict in sorted(nodes, key=lambda k: k['loc_y'], reverse=True)]
        if len(nodes) == 0:
            return {"FINISHED"}

        list_node = nt.nodes.new('RSNodeSettingsMergeNode')
        loc_x = numpy.mean([node.location[0] for node in nodes])
        loc_y = numpy.mean([node.location[1] for node in nodes])
        list_node.location = loc_x + 200, loc_y

        for i, node in enumerate(nodes):
            if i < 3:
                nt.links.new(node.outputs[0], list_node.inputs[i])
            else:
                list_node.inputs.new('RSNodeSocketTaskSettings', "Settings")
                nt.links.new(node.outputs[0], list_node.inputs[i])

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_MergeTask)
    bpy.utils.register_class(RSN_OT_MergeSettings)


def unregister():
    bpy.utils.unregister_class(RSN_OT_MergeTask)
    bpy.utils.unregister_class(RSN_OT_MergeSettings)
