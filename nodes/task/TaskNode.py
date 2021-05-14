import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import *
from ...preferences import get_pref


def update_node(self, context):
    if len(self.var_collect_list) != 0:
        self.update_parms()


def set_active_task(self, context):
    if self.is_active_task is True:
        bpy.context.window_manager.rsn_viewer_node = self.name
        print(f"RenderNode:Set Active Task: {self.name}")


class RSNodeTaskNode(RenderStackNode):
    """A simple Task node"""
    bl_idname = "RSNodeTaskNode"
    bl_label = 'Task'

    # set active and update
    ###############
    is_active_task: BoolProperty(default=False,
                                 update=set_active_task,
                                 description='Set as active Task')

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Settings")
        self.outputs.new('RSNodeSocketRenderList', "Task")
        self.label = self.name

        # bpy.ops.rsn.edit_var_collect(action="ADD", task_node_name=self.name)

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'label', text='')

        row.prop(self, 'is_active_task', text='', icon="HIDE_OFF" if self.is_active_task else "HIDE_ON")

    def update(self):
        self.auto_update_inputs('RSNodeSocketTaskSettings', "Settings")
        set_active_task(self, bpy.context)

    def get_data(self):
        var_collect_data = {}
        # var_collect_data['active_index'] = self.var_collect_list_index

        for i, collect in enumerate(self.var_collect_list):
            var_nodes = {}
            for item in collect.node_properties:
                var_nodes[item.name] = item.active

            var_collect_data[i] = var_nodes

        return var_collect_data


def update_viewer_tasks(self, context):
    try:
        nt = context.space_data.node_tree
    except AttributeError:
        return None

    for node in nt.nodes:
        if node.bl_idname == 'RSNodeTaskNode' and node.name != context.window_manager.rsn_viewer_node:
            node.is_active_task = False

    rsn_task = RSN_Nodes(node_tree=nt,
                         root_node_name=context.window_manager.rsn_viewer_node)

    node_list = rsn_task.get_children_from_node(rsn_task.root_node)  # VariantsNodeProperty node in each task
    # only one set VariantsNodeProperty node will be active
    var_collect = {}
    for node_name in node_list:
        set_var_node = rsn_task.nt.nodes[node_name]
        if set_var_node.bl_idname == 'RSNodeSetVariantsNode':
            for item in set_var_node.node_collect:
                if item.use:
                    var_collect[item.name] = item.active
            break

    for node_name, active in var_collect.items():
        var_node = rsn_task.nt.nodes[node_name]
        black_list = rsn_task.get_children_from_var_node(var_node, active)

        node_list = [i for i in node_list if i not in black_list]

    if len(node_list) > 0:
        node_list_str = ','.join(node_list)

        if bpy.context.window_manager.rsn_node_list != node_list_str:
            bpy.context.window_manager.rsn_node_list = node_list_str

            pref = get_pref()

            if rsn_task.root_node.inputs[0].is_linked:
                try:
                    bpy.context.window_manager.rsn_viewer_node = context.window_manager.rsn_viewer_node
                    bpy.ops.rsn.update_parms(view_mode_handler=context.window_manager.rsn_viewer_node,
                                             update_scripts=pref.node_viewer.update_scripts,
                                             use_render_mode=False)
                    # This error shows when the dragging the link off viewer node(Works well with knife tool)
                    # this seems to be a blender error

                except IndexError:
                    pass

            else:
                bpy.context.window_manager.rsn_viewer_node = ''


def register():
    bpy.utils.register_class(RSNodeTaskNode)

    bpy.types.WindowManager.rsn_node_list = StringProperty(default='')
    bpy.types.WindowManager.rsn_viewer_node = StringProperty(name='Viewer task name', update=update_viewer_tasks)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskNode)

    del bpy.types.WindowManager.rsn_node_list
    del bpy.types.WindowManager.rsn_viewer_node
