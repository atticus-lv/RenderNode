import bpy
from bpy.props import StringProperty, PointerProperty, EnumProperty, BoolProperty

from ...nodes.BASE.node_base import RenderNodeBase
from ...preferences import get_pref


def update_node(self, context):
    self.execute_tree()


class RenderNodeScripts(RenderNodeBase):
    '''A simple input node'''
    bl_idname = 'RenderNodeScripts'
    bl_label = 'Scripts'

    code: StringProperty(name='Code to execute', default='', update=update_node)

    def init(self, context):
        self.create_input('RenderNodeSocketString','code','Code')
        self.create_output('RSNodeSocketTaskSettings', 'Settings', 'Settings')
        self.width = 200

    def process(self, context, id, path):
        value = self.inputs['code'].get_value()
        try:
            exec(value)
        except Exception as e:
            print(e)


def register():
    bpy.utils.register_class(RenderNodeScripts)


def unregister():
    bpy.utils.unregister_class(RenderNodeScripts)
