import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeOctaneRenderSettingsNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeOctaneRenderSettingsNode'
    bl_label = 'Octane Settings'

    # kernel_type: EnumProperty(name='Octane Kernel Type',
    #                           items=[
    #                               ('0', 'Default', ''),
    #                               ('1', 'Direct light', ''),
    #                               ('2', 'Path trace', ''),
    #                               ('3', 'PMC', ''),
    #                               ('4', 'Info-channel', ''), ],
    #                           default='2')
    # # show when kernel in 0,1
    # gi_mode: EnumProperty(name='GImode',
    #                       items=[
    #                           ('0', 'None', ''),
    #                           ('3', 'Ambient occlusion', ''),
    #                           ('4', 'Diffuse', ''), ],
    #                       default='0')
    # clay_mode: EnumProperty(name='GImode',
    #                         items=[
    #                             ('None', 'None', ''),
    #                             ('Grey', 'Grey', ''),
    #                             ('Color', 'Color', ''), ],
    #                         default='None')
    # info_channel_type: StringProperty()

    show_sampling: BoolProperty(name='Samples', default=False)
    # quality
    max_samples: IntProperty(name='Max. samples', default=500, min=1, update=update_node)
    max_diffuse_depth: IntProperty(name='Max. diffuse depth', default=5, min=1, update=update_node)
    max_glossy_depth: IntProperty(name='Max. glossy depth', default=12, min=1, update=update_node)
    max_scatter_depth: IntProperty(name='Max. scatter depth', default=8, min=1, update=update_node)

    # adaptive_sampling
    adaptive_sampling: BoolProperty(name='Adaptive sampling', default=False, update=update_node)
    adaptive_noise_threshold: FloatProperty(name='Noise threshold', default=0.03, min=0, update=update_node)
    adaptive_min_samples: IntProperty(name='Min. adaptive samples', default=256, min=2, update=update_node)
    adaptive_group_pixels: EnumProperty(name='Group pixels',
                                        items=[
                                            ('1', 'None', ''),
                                            ('2', '2x2', ''),
                                            ('4', '4x4', ''), ],
                                        default='2', update=update_node)
    adaptive_expected_exposure: FloatProperty(name='Expected exposure', default=0, precision=4, update=update_node)

    # sampling
    path_term_power: FloatProperty(name='Path term. power', min=0.0, default=0.3, update=update_node)
    coherent_ratio: FloatProperty(name='Coherent ratio', min=0.0, default=0, update=update_node)
    static_noise: BoolProperty(name='Static noise', default=False, update=update_node)
    parallel_samples: IntProperty(name='Parallel samples', default=32, min=1, max=32, update=update_node)
    max_tile_samples: IntProperty(name='Max. tile samples', default=64, min=1, max=64, update=update_node)

    # seem to be 2.92's bug
    warning: BoolProperty(name='Is warning', default=False)
    warning_msg: StringProperty(name='warning message', default='')

    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)

        col = layout.column(align=1)

        col.prop(self, 'max_samples')
        col.prop(self, 'max_diffuse_depth')
        col.prop(self, 'max_glossy_depth')
        col.prop(self, 'max_scatter_depth')

        col.separator()
        box = col.box().split().column(align=1)
        box.prop(self, 'adaptive_sampling')
        if self.adaptive_sampling:
            box.prop(self, 'adaptive_noise_threshold')
            box.prop(self, 'adaptive_min_samples')
            box.prop(self, 'adaptive_group_pixels')
            box.prop(self, 'adaptive_expected_exposure')

        col.separator()
        box = col.box().split().column(align=1)
        box.prop(self, 'show_sampling', icon='TRIA_DOWN' if self.show_sampling else 'TRIA_RIGHT', emboss=False)
        if self.show_sampling:
            box.prop(self, 'path_term_power')
            box.prop(self, 'coherent_ratio')
            box.prop(self, 'static_noise')
            box.prop(self, 'parallel_samples')
            box.prop(self, 'max_tile_samples')

    def get_data(self):
        task_data = {}
        if 'octane' in bpy.context.preferences.addons:
            task_data['engine'] = "octane"
            task_data['octane'] = {
                # quality
                'max_samples'               : self.max_samples,
                'max_diffuse_depth'         : self.max_diffuse_depth,
                'max_glossy_depth'          : self.max_glossy_depth,
                'max_scatter_depth'         : self.max_scatter_depth,
                # adaptive_sampling
                'adaptive_sampling'         : self.adaptive_sampling,
                'adaptive_noise_threshold'  : self.adaptive_noise_threshold,
                'adaptive_group_pixels'     : self.adaptive_group_pixels,
                'adaptive_expected_exposure': self.adaptive_expected_exposure,
                # sampling
                'path_term_power'           : self.path_term_power,
                'coherent_ratio'            : self.coherent_ratio,
                'static_noise'              : self.static_noise,
                'parallel_samples'          : self.parallel_samples,
                'max_tile_samples'          : self.max_tile_samples,
            }
        else:
            self.set_warning()
            self.warning_msg = 'Octane Engine is not enable!'
        return task_data


def register():
    bpy.utils.register_class(RSNodeOctaneRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeOctaneRenderSettingsNode)
