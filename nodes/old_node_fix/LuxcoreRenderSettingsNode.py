import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RSNodeLuxcoreRenderSettingsNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodeLuxcoreRenderSettingsNode'
    bl_label = 'Luxcore Settings'

    use_samples: BoolProperty(name='Use Samples', default=True, update=update_node)
    use_time: BoolProperty(name='Use Time', default=False, update=update_node)

    time: IntProperty(default=300, min=1, name='Time(s)', update=update_node)
    samples: IntProperty(default=64, min=1, name="Samples", update=update_node)

    # seem to be 2.92's bug
    warning: BoolProperty(name='Is warning', default=False)
    warning_msg: StringProperty(name='warning message', default='')

    def init(self, context):
        self.warning = False
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 225

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)

        col = layout.column(align=1)
        row = col.row(align=True)
        row.prop(self, "use_samples")
        row.prop(self, "samples")

        row = col.row(align=True)
        row.prop(self, 'use_time')
        row.prop(self, 'time')
    
    def process(self, context, id, path):
        task_data = self.get_data()
        if 'luxcore_half' in task_data and 'BlendLuxCore' in bpy.context.preferences.addons:
            if not bpy.context.scene.luxcore.halt.enable:
                bpy.context.scene.luxcore.halt.enable = True

            if task_data['luxcore_half']['use_samples'] is False and task_data['luxcore_half'][
                'use_time'] is False:
                bpy.context.scene.luxcore.halt.use_samples = True

            elif task_data['luxcore_half']['use_samples'] is True and task_data['luxcore_half'][
                'use_time'] is False:
                if not bpy.context.scene.luxcore.halt.use_samples:
                    bpy.context.scene.luxcore.halt.use_samples = True
                if bpy.context.scene.luxcore.halt.use_time:
                    bpy.context.scene.luxcore.halt.use_time = False

                self.compare(bpy.context.scene.luxcore.halt, 'samples', task_data['luxcore_half']['samples'])

            elif task_data['luxcore_half']['use_samples'] is False and task_data['luxcore_half'][
                'use_time'] is True:
                if bpy.context.scene.luxcore.halt.use_samples:
                    bpy.context.scene.luxcore.halt.use_samples = False
                if not bpy.context.scene.luxcore.halt.use_time:
                    bpy.context.scene.luxcore.halt.use_time = True

                self.compare(bpy.context.scene.luxcore.halt, 'time', task_data['luxcore_half']['time'])
                
    def get_data(self):
        task_data = {}
        if 'BlendLuxCore' in bpy.context.preferences.addons:
            task_data['engine'] = 'LUXCORE'
            task_data['luxcore_half'] = {'use_samples': self.use_samples,
                                         'samples'    : self.samples,
                                         'use_time'   : self.use_time,
                                         'time'       : self.time}
        self.set_warning(msg= "Luxcore is not enabled")
        return task_data


def register():
    bpy.utils.register_class(RSNodeLuxcoreRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeLuxcoreRenderSettingsNode)
