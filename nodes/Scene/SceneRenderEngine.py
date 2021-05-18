import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RenderNodeSceneRenderEngine(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RenderNodeSceneRenderEngine'
    bl_label = 'Scene Render Engine'

    _enum_item_hack = []

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, "engine")

    def process(self):
        self.compare(bpy.context.scene.render, 'engine', self.engine)

    def engine_enum_items(self, context):
        enum_items = RenderNodeSceneRenderEngine._enum_item_hack
        enum_items.clear()

        # append viewport engine
        enum_items.append(('BLENDER_EEVEE', 'Eevee', ''))
        enum_items.append(('BLENDER_WORKBENCH', 'Workbench', ''))

        addon = [engine.bl_idname for engine in bpy.types.RenderEngine.__subclasses__()]

        # append to enum_items
        for name in addon:
            enum_items.append((name, name.capitalize(), ''))

        return enum_items

    temp = engine_enum_items

    engine: EnumProperty(name='Engine', description='Render Eninge available',
                         items=temp, update=update_node)


def register():
    bpy.utils.register_class(RenderNodeSceneRenderEngine)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneRenderEngine)
