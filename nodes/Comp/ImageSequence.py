import bpy
from bpy.props import *

import os
from ...nodes.BASE.node_base import RenderNodeBase
from ...nodes.BASE._runtime import runtime_info
from ...preferences import get_pref


def update_node(self, context):
    self.execute_tree()


class RenderNodeImageSequence(RenderNodeBase):
    bl_idname = "RenderNodeImageSequence"
    bl_label = 'Image Sequence'

    operate_type: EnumProperty(
        items=[
            ('IMG_2_MOV', 'Sequence to Movie', ''),
            ('MOV_2_IMG', 'Movie to Sequence', '')
        ],
        default='IMG_2_MOV', update=update_node)

    image: PointerProperty(type=bpy.types.Image, update=update_node)
    frame_duration: IntProperty(name='Frame Duration', update=update_node)
    frame_start: IntProperty(name='Frame Start', update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketInt', 'frame_duration', 'Frame Duration', default_value=1)
        self.create_input('RenderNodeSocketInt', 'frame_start', 'Frame Start', default_value=1)
        self.create_input('RenderNodeSocketInt', 'frame_offset', 'Frame Offset', default_value=0)
        self.create_input('RenderNodeSocketBool', 'use', 'Use', default_value=True)
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')
        layout.template_ID(self, "image", new="image.new", open="image.open")

    def process(self, context, id, path):
        if self.operate_type == 'IMG_2_MOV':
            self.compare(self.image, 'source', 'SEQUENCE')
        else:
            self.compare(self.image, 'source', 'MOVIE')

        scn = context.scene
        scn.use_nodes = True

        nt = context.scene.node_tree
        img_node = nt.nodes.get(self.name)

        if self.inputs['use'].get_value():
            if img_node is None:
                img_node = nt.nodes.new('CompositorNodeImage')
                img_node.name = self.name

            self.compare(img_node, 'image', self.image)
            img_node.frame_duration = self.inputs['frame_duration'].get_value()
            img_node.frame_start = self.inputs['frame_start'].get_value()
            img_node.frame_offset = self.inputs['frame_offset'].get_value()

            try:
                name = get_pref().node_view_layer_passes.comp_node_name
                com = context.scene.node_tree.nodes.get(name)
            except Exception:
                for node in context.scene.node_tree.nodes:
                    if node.bl_idname == 'CompositorNodeComposite':
                        context.scene.node_tree.nodes.remove(node)

                com = nt.nodes.new(type="CompositorNodeComposite")
                com.name = 'Composite'
                com.location = 430, 430

            nt.links.new(img_node.outputs[0], com.inputs[0])
        else:
            if img_node: nt.nodes.remove(img_node)


def register():
    bpy.utils.register_class(RenderNodeImageSequence)


def unregister():
    bpy.utils.unregister_class(RenderNodeImageSequence)
