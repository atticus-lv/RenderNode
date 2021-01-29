import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeWorldInputNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeWorldInputNode'
    bl_label = 'World'

    world: PointerProperty(name="World", type=bpy.types.World, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 150

    def draw_buttons(self, context, layout):
        layout.prop(self, 'world', text="")


def register():
    bpy.utils.register_class(RSNodeWorldInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeWorldInputNode)
