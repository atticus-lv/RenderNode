import bpy
from bpy.props import StringProperty, PointerProperty, EnumProperty
from RenderStackNode.node_tree import RenderStackNode


def update_node(self, context):
    self.update()


class RSNodeScriptsNode(RenderStackNode):
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
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, "type", expand=1)
        if self.type == 'SINGLE':
            layout.prop(self, "code", text="")
        else:
            layout.prop(self, "file", text="")


def register():
    bpy.utils.register_class(RSNodeScriptsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeScriptsNode)
