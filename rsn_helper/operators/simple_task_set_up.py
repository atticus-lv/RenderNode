import bpy
from bpy.props import IntProperty

class RSN_OT_SimpleTask(bpy.types.Operator):
    bl_idname = 'rsn.simple_task'
    bl_label = 'Simple Task'

    @classmethod
    def poll(self, context):
        return bpy.context.space_data.edit_tree and bpy.context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree
        x = 0
        y = 0

        task = nt.nodes.new('RSNodeTaskNode')
        cam = nt.nodes.new('RSNodeCamInputNode')
        eevee = nt.nodes.new('RSNodeEeveeRenderSettingsNode')
        path = nt.nodes.new('RSNodeFilePathInputNode')
        res = nt.nodes.new('RSNodeResolutionInputNode')
        merge_output = nt.nodes.new('RSNodeSettingsMergeNode')

        task.location = (x, y)
        cam.location = (x - 300, y)
        eevee.location = (x - 300, y - 100)
        path.location = (x - 550, y - 200)
        res.location = (x - 500, y - 350)
        merge_output.location = (x - 300, y - 200)

        for node in nt.nodes:
            node.select = 0

        task.select = 1
        cam.select = 1
        eevee.select = 1
        path.select = 1
        res.select = 1
        merge_output.select = 1

        nt.nodes.active = merge_output
        for i in range(2):
            bpy.ops.rsnode.edit_input(socket_type="RSNodeSocketOutputSettings", socket_name="Output Settings")

        nt.links.new(cam.outputs[0], task.inputs[0])
        nt.links.new(eevee.outputs[0], task.inputs[1])
        nt.links.new(merge_output.outputs[0], task.inputs[2])
        nt.links.new(path.outputs[0], merge_output.inputs[0])
        nt.links.new(res.outputs[0], merge_output.inputs[1])

        bpy.ops.node.join()
        frame = nt.nodes.active
        frame.label = 'Simple Task'

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_SimpleTask)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SimpleTask)
