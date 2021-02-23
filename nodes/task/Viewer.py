from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...utility import *
from ...preferences import get_pref


def reroute(node):
    def is_task_node(node):
        if node.bl_idname == "RSNodeTaskNode":
            return node
        sub_node = node.inputs[0].links[0].from_node
        return is_task_node(sub_node)

    task_node_name = is_task_node(node)
    return task_node_name


class RSN_OT_AddViewerNode(bpy.types.Operator):
    bl_idname = 'rsn.add_viewer_node'
    bl_label = 'Add Viewer Node'

    @classmethod
    def poll(self, context):
        if context.space_data.edit_tree:
            active_node = context.space_data.edit_tree.nodes.active
            return active_node and active_node.bl_idname == 'RSNodeTaskNode'

    def execute(self, context):
        nt = context.space_data.edit_tree
        task = context.space_data.edit_tree.nodes.active
        loc_x = task.location[0] + 200
        loc_y = task.location[1] + 25
        # remove viewer node
        for node in nt.nodes:
            if node.bl_idname == 'RSNodeViewerNode':
                context.space_data.edit_tree.nodes.remove(node)

        viewer = context.space_data.edit_tree.nodes.new(type='RSNodeViewerNode')
        viewer.location[0] = loc_x
        viewer.location[1] = loc_y

        nt.links.new(task.outputs[0], viewer.inputs[0])
        viewer.update()
        viewer.select = 0
        # force update
        dg = context.evaluated_depsgraph_get()
        dg.update()
        return {"FINISHED"}


class RSNodeViewerNode(RenderStackNode):
    bl_idname = 'RSNodeViewerNode'
    bl_label = 'Viewer'

    show_pref: BoolProperty(default=False)

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.width = 175

    def update(self):
        rsn_task = RSN_Nodes(node_tree=bpy.context.space_data.edit_tree,
                             root_node_name=self.name)
        node_list = rsn_task.get_children_from_node(self)
        if len(node_list) > 0:
            node_list_str = ','.join(node_list)

            if bpy.context.window_manager.rsn_node_list != node_list_str:
                bpy.context.window_manager.rsn_node_list = node_list_str

                pref = get_pref()

                if self.inputs[0].is_linked:
                    try:
                        node = reroute(self.inputs[0].links[0].from_node)
                        bpy.context.window_manager.rsn_viewer_node = node.name
                        bpy.ops.rsn.update_parms(view_mode_handler=node.name,
                                                 update_scripts=pref.node_viewer.update_scripts,
                                                 use_render_mode=False)
                        # This error shows when the dragging the link off viewer node(Works well with knife tool)
                        # this seems to be a blender error
                    except IndexError:
                        pass

                else:
                    bpy.context.window_manager.rsn_viewer_node = ''

    def free(self):
        print("Node removed", self)
        bpy.context.window_manager.rsn_viewer_node = ''

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        if self.inputs[0].is_linked and context.window_manager.rsn_viewer_node != '':
            node = context.space_data.edit_tree.nodes[context.window_manager.rsn_viewer_node]
            row.label(text=f'{node.name} | {node.label}', icon='NODE_SEL')

        else:
            row.label(text='', icon='NODE')

        layout.label(text=f'Update:{context.window_manager.rsn_tree_time}', icon='MOD_TIME')
        # preferences.
        pref = get_pref()
        row.prop(self, 'show_pref', icon_only=1, icon='TRIA_DOWN' if self.show_pref else "TRIA_LEFT")
        if self.show_pref:
            layout.prop(pref.node_viewer, 'update_scripts', toggle=1)
            layout.prop(pref.node_viewer, 'update_path', toggle=1)
            layout.prop(pref.node_viewer, 'update_view_layer_passes', toggle=1)

    def draw_buttons_ext(self, context, layout):
        box = layout.box()
        col = box.column(align=True)
        col.label(text="TIPS:")
        col.label(text='Not execute scripts node or email node')
        col.label(text='Use view operator in Task List Node to execute them')


def draw_menu(self, context):
    if context.space_data.edit_tree.nodes.active.bl_idname == 'RSNodeTaskNode':
        layout = self.layout
        layout.separator()
        layout.operator("rsn.add_viewer_node", text="View Task")


def register():
    bpy.utils.register_class(RSN_OT_AddViewerNode)
    bpy.utils.register_class(RSNodeViewerNode)

    bpy.types.WindowManager.rsn_node_list = StringProperty(default='')

    # bpy.types.NODE_MT_context_menu.prepend(draw_menu)


def unregister():
    bpy.utils.unregister_class(RSNodeViewerNode)

    del bpy.types.WindowManager.rsn_node_list
    # bpy.types.NODE_MT_context_menu.remove(draw_menu)
