import bpy
from bpy.props import IntProperty


class RSN_OT_SimpleTask(bpy.types.Operator):
    """A simple task example"""
    bl_idname = 'rsn.simple_task'
    bl_label = 'Simple Task'

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and bpy.context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def execute(self, context):
        nt = context.space_data.edit_tree
        x = 0
        y = 0

        task = nt.nodes.new('RSNodeTaskNode')
        cam = nt.nodes.new('RSNodeCamInputNode')
        eevee = nt.nodes.new('RSNodeEeveeRenderSettingsNode')
        path = nt.nodes.new('RSNodeFilePathInputNode')
        res = nt.nodes.new('RSNodeResolutionInputNode')
        # range = nt.nodes.new('RSNodeFrameRangeInputNode')
        merge_output = nt.nodes.new('RSNodeSettingsMergeNode')

        task.location = (x + 10, y)
        cam.location = (x - 200, y + 50)
        eevee.location = (x - 200, y - 50)
        path.location = (x - 500, y - 100)
        res.location = (x - 450, y - 250)
        # range.location = (x - 450, y - 380)
        merge_output.location = (x - 200, y - 150)

        for node in nt.nodes:
            node.select = 0
        task.select = 1
        cam.select = 1
        eevee.select = 1
        path.select = 1
        res.select = 1
        # range.select = 1
        merge_output.select = 1

        nt.links.new(cam.outputs[0], task.inputs[0])
        nt.links.new(eevee.outputs[0], task.inputs[1])
        nt.links.new(merge_output.outputs[0], task.inputs[2])
        nt.links.new(path.outputs[0], merge_output.inputs[0])
        nt.links.new(res.outputs[0], merge_output.inputs[1])
        # nt.links.new(range.outputs[0], merge_output.inputs[2])

        bpy.ops.node.join()
        frame = nt.nodes.active
        frame.label = 'Simple Task'

        return {"FINISHED"}


class RSN_OT_MoveNode(bpy.types.Operator):
    bl_idname = 'rsn.move_node'
    bl_label = 'Move Node'
    bl_options = {"UNDO", 'GRAB_CURSOR', 'BLOCKING'}

    frame = None

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and bpy.context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def invoke(self, context, event):
        bpy.ops.rsn.simple_task()

        nt = context.space_data.edit_tree
        self.frame = nt.nodes.active
        self.frame.location = context.space_data.cursor_location
        bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SimpleTask)
    bpy.utils.register_class(RSN_OT_MoveNode)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SimpleTask)
    bpy.utils.unregister_class(RSN_OT_MoveNode)
