from bpy.props import *
from ...utility import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...ui.icon_utils import RSN_Preview

from itertools import groupby

rsn_icon = RSN_Preview(image='RSN.png', name='rsn_icon')


class ProcessorBarProperty(bpy.types.PropertyGroup):
    # store data into node's property
    task_list: StringProperty()
    cur_task: StringProperty()
    # draw properties
    done_col: FloatVectorProperty(name='Done Color', subtype='COLOR', default=(0, 1, 0), min=1, max=1)
    wait_col: FloatVectorProperty(name='Wait Color', subtype='COLOR', default=(0, 0, 0), min=1, max=1)





class TaskProperty(bpy.types.PropertyGroup):
    name: StringProperty(
        default="",
        name="Task Node Name",
        description="Name of the node")

    render: BoolProperty(name="Render", default=True, description="Use for render")




# use uilist for visualization
class RSN_UL_RenderTaskList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        nt = context.space_data.node_tree

        node = nt.nodes.get(item.name)
        if node:
            row.prop(node, 'is_active_task', text='', emboss=False,
                     icon="HIDE_OFF" if node.is_active_task else "HIDE_ON")
        else:
            row.label(text='', icon='ERROR')

        row.label(text=item.name)

        frame_count = (1 + node.frame_end - node.frame_start) // node.frame_step
        row.label(
            text=f'{node.frame_start}~{node.frame_end}({frame_count})')

        row.prop(item, "render", text="", icon="CHECKMARK")


class RSN_OT_UpdateTaskList(bpy.types.Operator):
    """Update List item"""
    bl_idname = "rsn.update_task_list"
    bl_label = "Update List"

    render_list_name: StringProperty()

    def execute(self, context):
        self.get_task_list()
        return {"FINISHED"}

    def get_task_list(self):
        tree = RSN_Nodes(node_tree=bpy.context.space_data.node_tree, root_node_name=self.render_list_name)
        node_list = tree.get_children_from_node(root_node=tree.root_node)

        task_list = [name for name in node_list if
                     bpy.context.space_data.node_tree.nodes.get(name).bl_idname == 'RSNodeTaskNode']

        remain = {}  # dict for the remain nodes

        for i, key in enumerate(tree.root_node.task_list.keys()):
            if key not in task_list:
                tree.root_node.task_list.remove(i)  # remove unlink nodes
                tree.root_node.task_list_index -= 1 if tree.root_node.task_list_index != 0 else 0
            else:
                # save render attribute
                item = tree.root_node.task_list[i]
                attrs = {'render': item.render,
                         }
                remain[key] = attrs

        tree.root_node.task_list.clear()  # clear list then add it back

        for name in task_list:
            item = tree.root_node.task_list.add()
            item.name = name

            if name not in remain: continue

            attrs = remain[name]
            item.render = attrs['render']


def resize_node(self, context):
    if self.show_processor_bar:
        self.width *= 2
    else:
        self.width *= 0.5


class RSNodeRenderListNode(RenderStackNode):
    """Render List Node"""
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    # action after render
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='Clean filepath after render', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW',
        name='Display')

    task_list: CollectionProperty(name="Task Property", type=TaskProperty)
    task_list_index: IntProperty(default=0, min=0)

    # processor
    show_processor_bar: BoolProperty(name='Processor Bar', update=resize_node)
    processor_bar: PointerProperty(name="Processor Property", type=ProcessorBarProperty)

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.width = 175

    def draw_buttons(self, context, layout):

        # left
        split = layout.split(factor=0.5 if self.show_processor_bar else 1)
        col = split.column()

        col.operator("rsn.update_task_list", icon="FILE_REFRESH").render_list_name = self.name

        col.template_list(
            "RSN_UL_RenderTaskList", "Task List",
            self, "task_list",
            self, "task_list_index", )

        # properties
        box = col.box().column(align=1).box()
        item = self.task_list[self.task_list_index]
        node = context.space_data.node_tree.nodes[item.name]

        box.label(text=item.name, icon='ALIGN_TOP')
        row = box.column(align=1)
        row.prop(node, 'frame_start',text = "Frame Start")
        row.prop(node, 'frame_end')
        row.prop(node, 'frame_step')

        # bottom
        col.separator()
        row = col.row(align=1)
        row.scale_y = 1.25

        render = row.operator("rsn.render_stack_task", text=f'Render!',
                              icon='SHADING_RENDERED')  # icon_value=rsn_icon.get_image_icon_id()
        render.render_list_node_name = self.name

        row.prop(self, 'show_processor_bar', icon='PREFERENCES', text='')

        # right
        # settings bar
        if self.show_processor_bar:
            col = split.column()

            sub_col = col.box().column(align=1)
            sub_col.label(text='Render Action', icon='SETTINGS')
            sub_col.prop(self, 'open_dir')
            sub_col.prop(self, 'clean_path')
            sub_col.prop(context.scene.render, "use_lock_interface", toggle=False)
            sub_col.prop(self, 'render_display_type')

            col.separator()

            sub_col = col.box().column(align=1)
            self.draw_processor_bar(context, sub_col)

    def update(self):
        self.auto_update_inputs('RSNodeSocketRenderList', "Task")

    def draw_processor_bar(self, context, layout):
        bar = self.processor_bar

        task_list = bar.task_list.split(',')

        cur_id = task_list.index(bar.cur_task)
        total_process = (cur_id + 1) / len(task_list)

        col = layout.column(align=1)
        col.alignment = "CENTER"

        col.label(text=f'Process: {round(total_process * 100, 2)} %', icon='SORTTIME')
        sub = col.split(factor=total_process, align=1)
        sub.scale_y = 0.25
        sub.prop(bar, "done_col", text='')
        sub.prop(bar, "wait_col", text='')

        col = layout.column(align=1)
        # process of single task
        for index, task_name in enumerate(task_list):
            # finish list
            if index < cur_id:
                col.box().label(text=task_name, icon="CHECKBOX_HLT")
            # current
            elif index == cur_id:
                if not context.window_manager.rsn_running_modal:
                    box = col.box()
                    box.label(text=task_name, icon="CHECKBOX_HLT")
                    col.label(text='Render Finished!', icon='HEART')
                else:
                    row = col.box().row(align=1)
                    row.label(text=task_name, icon="RENDER_STILL")
                    row.label(text="Process:{:.2f}%".format(
                        context.scene.frame_current / (context.scene.frame_end + 1 - context.scene.frame_start)))
            # waiting
            elif index > cur_id:
                col.box().label(text=task_name, icon="CHECKBOX_DEHLT")


def register():
    rsn_icon.register()

    bpy.utils.register_class(ProcessorBarProperty)
    bpy.utils.register_class(TaskProperty)
    bpy.utils.register_class(RSN_UL_RenderTaskList)
    bpy.utils.register_class(RSN_OT_UpdateTaskList)
    bpy.utils.register_class(RSNodeRenderListNode)


def unregister():
    rsn_icon.unregister()

    bpy.utils.unregister_class(ProcessorBarProperty)
    bpy.utils.unregister_class(TaskProperty)
    bpy.utils.unregister_class(RSN_UL_RenderTaskList)
    bpy.utils.unregister_class(RSN_OT_UpdateTaskList)
    bpy.utils.unregister_class(RSNodeRenderListNode)
