import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
# from ...utility import source_attr
from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type == 'Object':
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_output('RenderNodeSocketXYZ', 'location', 'Location')
        self.create_output('RenderNodeSocketXYZ', 'scale', 'Scale')
        self.create_output('RenderNodeSocketEuler', 'rotate', 'Rotate')
    else:
        self.remove_input('object')
        self.remove_output('location')
        self.remove_output('scale')
        self.remove_output('rotate')

    if self.operate_type == 'Material':
        self.create_input('RenderNodeSocketMaterial', 'material', 'Material')
    else:
        self.remove_input('material')

    if self.operate_type == 'World':
        self.create_input('RenderNodeSocketWorld', 'world', 'World')
    else:
        self.remove_input('world')

    if self.operate_type == 'Collection':
        self.create_input('RenderNodeSocketCollection', 'collection', 'Collection')
        self.create_output('RenderNodeSocketInt', 'count', 'Objects Count')
    else:
        self.remove_input('collection')
        self.remove_output('count')

    if self.operate_type =='Action':
        self.create_input('RenderNodeSocketAction', 'action', 'Action')
    else:
        self.remove_input('action')

    self.execute_tree()


class RenderNodeInfoInput(RenderNodeBase):
    bl_idname = 'RenderNodeInfoInput'
    bl_label = 'Information Input'

    operate_type: EnumProperty(name='Type', items=[
        ('Object', 'Object', ''),
        ('Material', 'Material', ''),
        ('World', 'World', ''),
        ('Collection', 'Collection', ''),
        ('Action', 'Action', ''),
    ], default='Object', update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', 'Object')
        self.create_output('RenderNodeSocketString', 'name', "Name")
        self.create_output('RenderNodeSocketXYZ', 'location', 'Location')
        self.create_output('RenderNodeSocketXYZ', 'scale', 'Scale')
        self.create_output('RenderNodeSocketEuler', 'rotate', 'Rotate')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        pointer = self.inputs[0].get_value()
        if pointer is None: return

        self.outputs['name'].set_value(pointer.name)

        if self.operate_type == 'Object':
            self.outputs['location'].set_value(pointer.location)
            self.outputs['scale'].set_value(pointer.scale)
            self.outputs['rotate'].set_value(pointer.rotation_euler)
        elif self.operate_type == 'Material':
            return
        elif self.operate_type == 'World':
            return
        elif self.operate_type == 'Collection':
            self.outputs['count'].set_value(len(pointer.objects))


def register():
    bpy.utils.register_class(RenderNodeInfoInput)


def unregister():
    bpy.utils.unregister_class(RenderNodeInfoInput)
