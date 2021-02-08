import bpy
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class WorkBenchRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeWorkBenchRenderSettingsNode'
    bl_label = 'WorkBench Settings'


    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        pass

    def get_data(self):
        task_data = {}
        task_data['engine'] = 'BLENDER_WORKBENCH'
        return task_data

def register():
    bpy.utils.register_class(WorkBenchRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(WorkBenchRenderSettingsNode)
