import bpy
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class WorkBenchRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeWorkBenchRenderSettingsNode'
    bl_label = 'WorkBench Settings'

    # render_aa: EnumProperty(name='Samples',
    #                         items=[('OFF', 'No Anti-Aliasing', ''),
    #                                ('FXAA', 'Single Pass Anti-Aliasing'),
    #                                ('5', '5 Samples'),
    #                                ('8', '8 Samples'),
    #                                ('11', '11 Samples'),
    #                                ('16', '16 Samples'),
    #                                ('32', '32 Samples'),
    #                                ])

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        # layout.prop(self,'render_aa')
        pass

def register():
    bpy.utils.register_class(WorkBenchRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(WorkBenchRenderSettingsNode)
