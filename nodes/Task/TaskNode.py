import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase
from ...utility import *
from ...preferences import get_pref


def update_node(self, context):
    if len(self.var_collect_list) != 0:
        self.update_parms()


def set_active_task(self, context):
    if self.is_active_task is True:
        self.execute_dependants()
        self.execute()


def correct_task_frame(self, context):
    if self.is_active_task:
        compare(context.scene, 'frame_start', self.frame_start)
        compare(context.scene, 'frame_end', self.frame_end)
        compare(context.scene, 'frame_step', self.frame_step)


class RSNodeTaskNode(RenderNodeBase):
    """A simple Task node"""
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    # get necessary props from some nodes
    ##################
    # path
    path: StringProperty(name='File Path', default='/tmp/', subtype='FILE_PATH')
    # frame
    frame_start: IntProperty(
        default=1,
        name="Start", description="Frame Start", update=correct_task_frame)
    frame_end: IntProperty(
        default=1,
        name="End", description="Frame End", update=correct_task_frame)
    frame_step: IntProperty(
        default=1,
        name="Step", description="Frame Step", update=correct_task_frame)

    # set active and update
    ###############
    is_active_task: BoolProperty(default=False,
                                 update=set_active_task,
                                 description='Set as active Task')

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")
        self.label = self.name

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'label', text='')
        row.prop(self, 'is_active_task', text='', icon="HIDE_OFF" if self.is_active_task else "HIDE_ON")

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Settings")
        set_active_task(self, bpy.context)

    def process(self):
        # set necessary props
        bpy.context.scene.frame_start = self.frame_start
        bpy.context.scene.frame_end = self.frame_end
        bpy.context.scene.frame_step = self.frame_step

        self.compare(bpy.context.scene.render, 'filepath', self.path)

        for node in self.id_data.nodes:
            if node.bl_idname == self.bl_idname and node != self:
                node.is_active_task = False

        # set active task
        bpy.context.window_manager.rsn_viewer_node = self.name


class RSN_OT_AddViewerNode(bpy.types.Operator):
    bl_idname = 'rsn.add_viewer_node'
    bl_label = 'Set Active Task'

    def execute(self, context):
        try:
            nt = context.space_data.edit_tree
            node = context.space_data.edit_tree.nodes.active
            if node.bl_idname == 'RSNodeTaskNode':
                node.is_active_task = True
        except:
            pass

        return {"FINISHED"}


# TODO Need to fix variant nodes


def register():
    bpy.utils.register_class(RSNodeTaskNode)
    bpy.utils.register_class(RSN_OT_AddViewerNode)

    bpy.types.WindowManager.rsn_viewer_node = StringProperty(name='Viewer task name')


def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)
    bpy.utils.unregister_class(RSN_OT_AddViewerNode)

    del bpy.types.WindowManager.rsn_viewer_node
