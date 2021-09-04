import bpy
import os

from bpy.props import IntProperty
from ... import __folder_name__
from ...nodes.BASE._runtime import runtime_info

default_value = {
    'Base Path': '//',
    'Camera': None,
    'Frame End': 1,
    'Frame Start': 1,
    'Frame Step': 1,
    'Path Exp': '$blend/$V/$camera.$F4',
    'Resolution %': 100,
    'Resolution Radio': 1.778,
    'Resolution Y': 1080,
    'Version': 0,
}


class RSN_OT_SimpleTask(bpy.types.Operator):
    """A simple task example"""
    bl_idname = 'rsn.simple_task'
    bl_label = 'Simple Task'

    @classmethod
    def poll(self, context):
        return context.space_data.edit_tree and bpy.context.space_data.edit_tree.bl_idname == 'RenderStackNodeTree'

    def get_preset(self):
        base_dir = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons', __folder_name__, 'preset',
                                'node_groups',
                                'simple_task.blend')

        node_group_dir = os.path.join(base_dir, 'NodeTree') + '/'
        node_preset_name = 'Simple Setting'

        if node_preset_name in bpy.data.node_groups:
            preset_node = bpy.data.node_groups[node_preset_name]
        else:
            bpy.ops.wm.append(filename=node_preset_name, directory=node_group_dir)
            preset_node = bpy.data.node_groups[node_preset_name]

        text_dir = os.path.join(base_dir, 'Text') + '/'
        text_name = 'RSN_tips'
        if text_name in bpy.data.texts:
            preset_tips = bpy.data.texts[text_name]
        else:
            bpy.ops.wm.append(filename=text_name, directory=text_dir)
            preset_tips = bpy.data.texts[text_name]

        return preset_node, preset_tips

    def execute(self, context):
        runtime_info['executing'] = True
        try:
            preset_node, preset_tips = self.get_preset()
            nt = context.space_data.edit_tree
            x = 0
            y = 0

            task = nt.nodes.new('RenderNodeTask')
            engine = nt.nodes.new('RenderNodeSceneRenderEngine')

            tips = nt.nodes.new('NodeFrame')
            tips.label = 'Tips'
            tips.text = preset_tips
            tips.width = 220
            tips.height = 360

            node_group = nt.nodes.new('RenderNodeGroup')
            node_group.node_tree_selection = preset_node
            node_group.width = 200

            for input in node_group.inputs:
                input.default_value = default_value[input.name]

            task.location = (x + 10, y)
            engine.location = (x - 160, y)
            node_group.location = (x - 220, y - 150)
            tips.location = (x + 10, y - 180)

            for node in nt.nodes:
                node.select = 0

            task.select = 1
            engine.select = 1
            tips.select = 1
            node_group.select = 1

            nt.links.new(engine.outputs[0], task.inputs[2])
            nt.links.new(node_group.outputs[0], task.inputs[3])

            bpy.ops.node.join()
            frame = nt.nodes.active
            frame.label = 'Simple Task'

        except Exception as e:
            print(e)
        finally:
            runtime_info['executing'] = False

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
