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


class RSNodeViewerNode(RenderStackNode):
    bl_idname = 'RSNodeViewerNode'
    bl_label = 'Viewer'
    bl_icon = 'HIDE_OFF'

    show_pref: BoolProperty(default=False)

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.width = 175

    def draw_label(self):
        return f'Task: {bpy.context.window_manager.rsn_viewer_node}'

    def update(self):
        pass

    def free(self):
        bpy.context.window_manager.rsn_viewer_node = ''

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)

        if context.scene.RSNBusyDrawing is True:
            draw = row.prop(context.scene, 'RSNBusyDrawing', text='Draw Nodes', toggle=1, icon='GREASEPENCIL')
        else:
            row.operator("rsn.draw_nodes", icon='GREASEPENCIL')

        # preferences.
        pref = get_pref()
        row.prop(self, 'show_pref', icon_only=1, icon='TRIA_DOWN' if self.show_pref else "TRIA_LEFT")
        if self.show_pref:
            layout.prop(pref.node_task, 'update_scripts', toggle=1)
            layout.prop(pref.node_task, 'update_path', toggle=1)
            layout.prop(pref.node_task, 'update_view_layer_passes', toggle=1)

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
    bpy.utils.register_class(RSNodeViewerNode)

    # bpy.types.NODE_MT_context_menu.prepend(draw_menu)


def unregister():
    bpy.utils.unregister_class(RSNodeViewerNode)

    # bpy.types.NODE_MT_context_menu.remove(draw_menu)
