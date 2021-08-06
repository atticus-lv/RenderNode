import bpy
from bpy.props import IntProperty
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.update_parms()


class RenderNodeSceneRenderSlot(RenderNodeBase):
    bl_idname = "RenderNodeSceneRenderSlot"
    bl_label = 'Scene Render Slot'

    def init(self, context):
        self.creat_input('RenderNodeSocketInt', 'slot_index', 'Slot', default_value=1)
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

    def process(self):
        render_result = bpy.data.images.get('Render Result')
        if not render_result: return None

        if self.inputs['slot_index'] < 1:
            self.inputs['slot_index'] = 1

        elif self.inputs['slot_index'] > len(render_result.render_slots):
            self.inputs['slot_index'] = len(render_result.render_slots)

        self.store_data()
        self.compare(render_result.render_slots, 'active_index', self.node_dict['slot_index'] - 1)


def register():
    bpy.utils.register_class(RenderNodeSceneRenderSlot)


def unregister():
    bpy.utils.unregister_class(RenderNodeSceneRenderSlot)
