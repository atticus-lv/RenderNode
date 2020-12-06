import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

from .TaskListNode import reroute

class RSN_OT_ViewerHandler(bpy.types.Operator):
    bl_idname = "rsn.viewer_handler"
    bl_label = 'Auto Update'

    _timer = None

    @classmethod
    def poll(self, context):
        return context.window_manager.rsn_viewer_modal is False

    def finish(self, context):
        context.window_manager.event_timer_remove(self._timer)
        context.window_manager.rsn_viewer_modal = False
        self.report({"INFO"}, 'Stop Auto Update')

    def modal(self, context, event):
        rsn_viewer_modal = context.window_manager.rsn_viewer_modal
        if not rsn_viewer_modal:
            self.finish(context)
            return {'FINISHED'}

        elif event.type == 'TIMER':
            if not rsn_viewer_modal:
                self.finish(context)
                return {"FINISHED"}
            else:
                bpy.ops.rsn.update_parms(task_name = context.window_manager.rsn_viewer_node )

        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.rsn_viewer_modal = True
        freq = 1
        self._timer = context.window_manager.event_timer_add(freq, window=context.window)
        context.window_manager.modal_handler_add(self)

        self.report({"INFO"}, 'Start Auto Correct EV')
        return {'RUNNING_MODAL'}


class RSNodeViewNode(RenderStackNode):
    bl_idname = 'RSNodeViewNode'
    bl_label = 'Viewer'

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            node = reroute(input.links[0].from_node)
            context.window_manager.rsn_viewer_node = node.name
            layout.label(text = f'Viewing {node.name}')

def register():
    bpy.utils.register_class(RSNodeViewNode)
    bpy.types.WindowManager.rsn_viewer_modal = BoolProperty(name='Viewer Auto Update', default=False)
    bpy.types.WindowManager.rsn_viewer_node = StringProperty(name = 'Viewer task name')


def unregister():
    bpy.utils.unregister_class(RSNodeViewNode)
