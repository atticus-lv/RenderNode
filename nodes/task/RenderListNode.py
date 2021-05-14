from bpy.props import *
from ...utility import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...ui.icon_utils import RSN_Preview

rsn_icon = RSN_Preview(image='RSN.png', name='rsn_icon')


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
        row.label(text=item.name, icon="NODE")
        row.prop(item, "render", text="", icon="CHECKMARK")


class RSN_OT_UpdateTaskList(bpy.types.Operator):
    """Update List item"""
    bl_idname = "rsn.update_task_list"
    bl_label = "Update"

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
                remain[key] = tree.root_node.task_list[i].render  # save render attribute

        tree.root_node.task_list.clear()  # clear list then add it back

        for name in task_list:
            item = tree.root_node.task_list.add()
            item.name = name
            if name in remain: item.render = remain[name]


class RSNodeRenderListNode(RenderStackNode):
    """Render List Node"""
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    # action after render
    show_action: BoolProperty(default=False)
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='Clean filepath after render', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW',
        name='Display')

    processor_node: StringProperty(name='Processor', default='')

    task_list: CollectionProperty("Task Property", type=TaskProperty)
    task_list_index: IntProperty(default=0, min=0)

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.width = 250

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)

        col.template_list(
            "RSN_UL_RenderTaskList", "Task List",
            self, "task_list",
            self, "task_list_index", )

        # call render button when selected

        col = layout.column(align=1)
        row = col.row(align=1)
        row.scale_y = 1.25
        row.scale_x = 1.15

        render = row.operator("rsn.render_stack_task", text=f'Render!', icon_value=rsn_icon.get_image_icon_id())
        render.render_list_node_name = self.name

        row.operator("rsn.update_task_list", text='Refresh', icon="FILE_REFRESH").render_list_name = self.name

        row.prop(self, "show_action", icon="TRIA_DOWN" if self.show_action else "TRIA_LEFT", text='')
        if self.show_action:
            col = col.box().split().column(align=1)
            col.prop(self, 'open_dir')
            col.prop(self, 'clean_path')
            col.prop(context.scene.render, "use_lock_interface", toggle=False)
            col.prop(self, 'render_display_type')

    def update(self):
        self.auto_update_inputs('RSNodeSocketRenderList', "Task")


def register():
    rsn_icon.register()

    bpy.utils.register_class(TaskProperty)
    bpy.utils.register_class(RSN_UL_RenderTaskList)
    bpy.utils.register_class(RSN_OT_UpdateTaskList)
    bpy.utils.register_class(RSNodeRenderListNode)


def unregister():
    rsn_icon.unregister()

    bpy.utils.unregister_class(TaskProperty)
    bpy.utils.unregister_class(RSN_UL_RenderTaskList)
    bpy.utils.unregister_class(RSN_OT_UpdateTaskList)
    bpy.utils.unregister_class(RSNodeRenderListNode)
