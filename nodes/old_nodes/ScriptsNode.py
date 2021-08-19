import bpy
from bpy.props import StringProperty, PointerProperty, EnumProperty, BoolProperty

from ...nodes.BASE.node_base import RenderNodeBase
from ...preferences import get_pref


def update_node(self, context):
    self.execute_tree()


class RSNodeScriptsNode(RenderNodeBase):
    '''A simple input node'''
    bl_idname = 'RSNodeScriptsNode'
    bl_label = 'Scripts'

    code: StringProperty(name='Code to execute', default='', update=update_node)
    file: PointerProperty(type=bpy.types.Text, name="Scripts file", update=update_node)

    type: EnumProperty(
        name='Type',
        items=[
            ('SINGLE', 'Single', ''), ('FILE', 'File', '')
        ],
        default='SINGLE'
    )

    def init(self, context):
        self.create_input('RenderNodeSocketString','code','Code')
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, "type", expand=1)
        if self.type == 'SINGLE':
            layout.prop(self, "code", text="")
        else:
            layout.prop(self, "file", text="")

    def process(self, context, id, path):
        value = self.code if self.type == 'SINGLE' else self.file.as_string()
        try:
            exec(value)
        except Exception as e:
            print(e)


def register():
    bpy.utils.register_class(RSNodeScriptsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeScriptsNode)
