import bpy
from RenderStackNode.node_tree import RenderStackNode


def update_node(self, context):
    self.update()


class WorkBenchRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeWorkBenchRenderSettingsNode'
    bl_label = 'WorkBench Settings'

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings", update=update_node)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(WorkBenchRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(WorkBenchRenderSettingsNode)
