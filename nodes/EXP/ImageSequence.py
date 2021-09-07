import bpy
from bpy.props import *

import os
from ...nodes.BASE.node_base import RenderNodeBase
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
        self.create_input('RenderNodeSocketFilePath', 'path', 'Path')
        self.create_input('RenderNodeSocketInt', 'frame_duration', 'Frame Duration', default_value=1)
        self.create_input('RenderNodeSocketInt', 'frame_start', 'Frame Start', default_value=0)
        self.create_input('RenderNodeSocketBool', 'use', 'Use', default_value=True)
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

        if self.image:
            img = self.image
            layout.template_preview(img)

    def process(self, context, id, path):
        p = self.inputs['path'].get_value()
        if p and os.path.isfile(p):
            dir, filename = os.path.split(p)
            if filename not in bpy.data.images: bpy.data.images.load(p, check_existing=False)
            img = bpy.data.images.get(filename)
            self.compare(self, 'image', img)

        if self.image:
            if self.operate_type == 'IMG_2_MOV':
                self.compare(self.image, 'source', 'SEQUENCE')
            else:
                self.compare(self.image, 'source', 'MOVIE')

            self.create_comp(context, self.inputs['use'].get_value(), self.image.name)

    def create_comp(self, context, use, img_name):
        scn = context.scene
        scn.use_nodes = True

        nt = context.scene.node_tree
        img_node = nt.nodes.get(self.name)

        if use:
            if img_node is None:
                img_node = nt.nodes.new('CompositorNodeImage')
                img_node.name = self.name

            self.compare(img_node, 'image', bpy.data.images.get(img_name))
            self.compare(img_node, 'frame_duration', self.inputs['frame_duration'].get_value())
            self.compare(img_node, 'frame_start', self.inputs['frame_start'].get_value())

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
