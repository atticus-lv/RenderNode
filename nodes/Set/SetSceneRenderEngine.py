import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RenderNodeSetSceneRenderEngine(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeSetSceneRenderEngine'
    bl_label = 'Set Scene Render Engine'

    _enum_item_hack = []

    # cycles:
    cycles_device: EnumProperty(name='Device',
                                items=[('CPU', 'CPU', ''),
                                       ('GPU', 'GPU', ''), ],
                                default='GPU',
                                update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

    def draw_buttons(self, context, layout):
        layout.prop(self, "engine")
        if self.engine == 'CYCLES':
            layout.prop(self, 'cycles_device')

    def process(self, context, id, path):
        if not self.process_task():return
        self.compare(bpy.context.scene.render, 'engine', self.engine)

    def engine_enum_items(self, context):
        enum_items = RenderNodeSetSceneRenderEngine._enum_item_hack
        enum_items.clear()

        # append viewport engine
        enum_items.append(('BLENDER_EEVEE', 'Eevee', ''))
        enum_items.append(('BLENDER_WORKBENCH', 'Workbench', ''))
        enum_items.append(('CYCLES', 'Cycles', ''))

        addon = [engine.bl_idname for engine in bpy.types.RenderEngine.__subclasses__()]

        if len(addon) > 1: enum_items.append(None)  # add separator

        # append to enum_items
        for name in addon:
            if name != 'CYCLES': enum_items.append((name, name.capitalize(), ''))

        return enum_items

    temp_engine = engine_enum_items
    engine: EnumProperty(name='Engine', description='Render Eninge available',
                         items=temp_engine,
                         update=update_node)


def register():
    bpy.utils.register_class(RenderNodeSetSceneRenderEngine)


def unregister():
    bpy.utils.unregister_class(RenderNodeSetSceneRenderEngine)
