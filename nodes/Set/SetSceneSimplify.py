import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase

size = {
    'OFF': 'No Limited',
    '128': '128',
    '256': '256',
    '512': '512',
    '1024': '1024',
    '2048': '2048',
    '4096': '4096',
    '8192': '8192',

}


class RenderNodeSetSceneSimplify(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneSimplify'
    bl_label = 'Set Scene Simplify'

    use_cycles: BoolProperty()

    texture_limit: EnumProperty(name='Viewport Texuture Limited',
                                items=[(k, v, '') for k, v in size.items()], default='OFF')
    texture_limit_render: EnumProperty(name='Render Texuture Limited',
                                       items=[(k, v, '') for k, v in size.items()], default='OFF')

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketString', 'engine', 'Render Engine')

        self.create_input('RenderNodeSocketBool', 'use_simplify', 'Enable', default_value=False)
        self.create_input('RenderNodeSocketInt', 'simplify_subdivision', 'Max Subdivision', default_value=6)
        self.create_input('RenderNodeSocketFloat', 'simplify_child_particles', 'Max Child Particles', default_value=1)
        self.create_input('RenderNodeSocketFloat', 'simplify_volumes', 'Volumes Resolution', default_value=1)

        self.create_input('RenderNodeSocketInt', 'simplify_subdivision_render', 'Render Max Subdivision',
                          default_value=6)
        self.create_input('RenderNodeSocketFloat', 'simplify_child_particles_render', 'Render Max Child Particles',
                          default_value=1)

        self.create_input('RenderNodeSocketBool', 'use_camera_cull', 'Camera Culling', default_value=False)
        i = self.create_input('RenderNodeSocketFloat', 'camera_cull_margin', 'Camera Cull Margin', default_value=0.2)
        i.hide = True

        self.create_input('RenderNodeSocketBool', 'use_distance_cull', 'Distance Culling', default_value=False)
        i = self.create_input('RenderNodeSocketFloat', 'distance_cull_margin', 'Distance Cull Margin', default_value=50)
        i.hide = True

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 200

    def draw_buttons(self, context, layout):
        if self.use_cycles:
            layout.prop(self, 'texture_limit')
            layout.prop(self, 'texture_limit_render')

    def process(self, context, id, path):
        if not self.process_task(): return

        engine = self.inputs['engine'].get_value()

        if engine == 'CYCLES':
            self.use_cycles = True
            self.compare(context.scene.cycels, 'texture_limit', self.texture_limit)
            self.compare(context.scene.cycels, 'texture_limit_render', self.texture_limit_render)

            c = [
                'use_camera_cull',
                'camera_cull_margin',
                'use_distance_cull',
                'distance_cull_margin',
            ]

            for name in c:
                input = self.inputs.get(name)
                input.hide = False
                key = input.name
                value = input.get_value()
                if value is not None:
                    self.compare(context.scene.cycles, key, value)

        for input in self.inputs:
            key = input.name
            value = input.get_value()
            self.compare(context.scene.render, key, value)


def register():
    bpy.utils.register_class(RenderNodeSetSceneSimplify)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetSceneSimplify)
