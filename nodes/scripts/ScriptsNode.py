import bpy
from bpy.props import StringProperty, PointerProperty, EnumProperty, BoolProperty

from ...nodes.BASE.node_tree import RenderStackNode
from ...preferences import get_pref


def update_node(self, context):
    self.update_parms()


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

    warning: BoolProperty(name='Is warning', default=False)
    warning_msg: StringProperty(name='warning message', default='')

    def init(self, context):
        self.warning = False
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)

        layout.prop(self, "type", expand=1)
        if self.type == 'SINGLE':
            layout.prop(self, "code", text="")
        else:
            layout.prop(self, "file", text="")

        pref = get_pref()
        if not pref.node_task.update_scripts:
            layout.label(text='Update is disable in viewer node', icon='ERROR')

    def get_data(self):
        task_data_obj = {}
        task_data_obj[self.name] = self.code if self.type == 'SINGLE' else self.file.name

        return task_data_obj


def register():
    bpy.utils.register_class(RSNodeScriptsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeScriptsNode)
