import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode
from RenderStackNode.utility import *

from .TaskListNode import reroute


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
        loc_y = task.location[1] + 100
        viewer = None
        for node in nt.nodes:
            if node.bl_idname == 'RSNodeViewerNode':
                viewer = node
                break
        if not viewer:
            viewer = context.space_data.edit_tree.nodes.new(type='RSNodeViewerNode')
        viewer.location[0] = loc_x
        viewer.location[1] = loc_y
        nt.links.new(task.outputs[0], viewer.inputs[0])

        return {"FINISHED"}


class RSNodeViewerNode(RenderStackNode):
    bl_idname = 'RSNodeViewerNode'
    bl_label = 'Viewer'

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")

    def free(self):
        print("Node removed", self)
        bpy.context.window_manager.rsn_viewer_modal = False

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            node = reroute(self.inputs[0].links[0].from_node)
            context.window_manager.rsn_viewer_node = node.name
            layout.label(text=f'Viewing {node.name}')

        else:
            context.window_manager.rsn_viewer_node = ''
            layout.label(text=f'Viewing Nothing')

    def draw_buttons_ext(self, context, layout):
        box = layout.box()
        col = box.column(align=True)
        col.label(text="TIPS:")
        col.label(text='Auto Update will not execute scripts node or email node')
        col.label(text='Use view operator in Task List Node to execute them')


addon_keymaps = []


def add_keybind():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('rsn.add_viewer_node', 'V', 'PRESS')
        addon_keymaps.append((km, kmi))


def remove_keybind():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("rsn.add_viewer_node", text="View Task")


def register():
    bpy.utils.register_class(RSN_OT_AddViewerNode)
    bpy.utils.register_class(RSNodeViewerNode)
    bpy.types.WindowManager.rsn_viewer_modal = BoolProperty(name='Viewer Auto Update', default=False)
    bpy.types.WindowManager.rsn_viewer_node = StringProperty(name='Viewer task name')

    bpy.types.NODE_MT_context_menu.prepend(draw_menu)
    add_keybind()


def unregister():
    del bpy.types.WindowManager.rsn_viewer_modal
    del bpy.types.WindowManager.rsn_viewer_node
    bpy.utils.unregister_class(RSNodeViewerNode)
    bpy.utils.unregister_class(RSN_OT_ViewerHandler)

    bpy.types.NODE_MT_context_menu.remove(draw_menu)
    remove_keybind()
