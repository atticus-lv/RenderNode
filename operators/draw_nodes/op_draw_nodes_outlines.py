from math import cos, sin, pi

import bgl
import blf
import bpy
import gpu

from bpy.props import *
from bpy.types import Operator
from gpu_extras.batch import batch_for_shader

from .utils import dpifac, draw_tri_fan
from ...preferences import get_pref
from ...nodes.BASE._runtime import cache_node_times, cache_node_dependants, curr_draw_handle, curr_draw_timer
from ...nodes.BASE.node_base import cache_executed_nodes

easy_name = {
    'BLENDER_EEVEE': 'Eevee',
    'BLENDER_WORKBENCH': 'WorkBench',
    'octane': 'Octane',
    'LUXCORE': 'Luxcore',
}


def find_node_parent(node):
    def get_parent(obj):
        if hasattr(obj, "parent"):
            get_parent(obj.parent)
        else:
            return obj

    return get_parent(node)


def get_node_location(node):
    nlocx = (node.location.x + 1) * dpifac()
    nlocy = (node.location.y + 1) * dpifac()
    ndimx = node.dimensions.x
    ndimy = node.dimensions.y

    return nlocx, nlocy, ndimx, ndimy


def get_node_vertices(node):
    nlocx = (node.location.x + 1) * dpifac()
    nlocy = (node.location.y + 1) * dpifac()
    ndimx = node.dimensions.x
    ndimy = node.dimensions.y

    if node.hide:
        nlocx += -1
        nlocy -= 10
    if node.type == 'REROUTE':
        # nlocx += 1
        nlocy -= 1
        ndimx = 0
        ndimy = 0

    if node.hide is True:
        top_left = (nlocx, nlocy + ndimy / 2)
        top_right = (nlocx + ndimx, nlocy + ndimy / 2)
        bottom_left = (nlocx, nlocy - ndimy / 2)
        bottom_right = (nlocx + ndimx, nlocy - ndimy - ndimy / 2)
    else:
        top_left = (nlocx, nlocy)
        top_right = (nlocx + ndimx, nlocy)
        bottom_left = (nlocx, nlocy - ndimy)
        bottom_right = (nlocx + ndimx, nlocy - ndimy)

    return top_left, top_right, bottom_left, bottom_right


def draw_text_2d(color, text, x, y, size=20):
    font_id = 0
    blf.position(font_id, x, y, 0)
    blf.color(font_id, color[0], color[1], color[2], color[3])
    blf.size(font_id, size, 72)
    blf.draw(font_id, text)


def draw_text_on_node(color, text, node, size=15, corner_index=1, offset=(0, 0)):
    '''index 0,1,2,3: top_left, top_right, bottom_left, bottom_right'''
    corners = get_node_vertices(node)
    pos = corners[corner_index]

    loc_x, loc_y = bpy.context.region.view2d.view_to_region(pos[0], pos[1], clip=False)
    draw_text_2d(color, text, loc_x + offset[0], loc_y + offset[1], size)


# TODO make draw outline when executing
def draw_callback_nodeoutline(self, context):
    bgl.glLineWidth(1)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glHint(bgl.GL_LINE_SMOOTH_HINT, bgl.GL_NICEST)

    # set color
    c1 = get_pref().draw_nodes.text_color1
    c2 = get_pref().draw_nodes.text_color2
    c3 = get_pref().draw_nodes.text_color3
    white = (c1[0], c1[1], c1[2], self.alpha)
    green = (c2[0], c2[1], c2[2], self.alpha)
    red = (c3[0], c3[1], c3[2], self.alpha)

    list_node = context.space_data.edit_tree.nodes.get(context.window_manager.rsn_active_list)
    if not list_node: return

    node_list = [node for node in context.space_data.edit_tree.nodes if node in cache_executed_nodes]
    try:
        for node in node_list:
            # draw time
            if node.id_data in cache_node_times:
                if node in cache_node_times[node.id_data]:
                    times = cache_node_times[node.id_data][node]
                    t = times['Execution'] if node.bl_idname != 'RenderNodeGroup' else times['Group']
                    t = t * 1000
                    if t < 0.1:
                        col = white
                    elif t < 1:
                        col = green
                    else:
                        col = red
                    draw_text_on_node(white, node.bl_label, node, size=17, corner_index=0, offset=(0, 3))
                    draw_text_on_node(col, f"{t:.2f}ms", node, size=12, corner_index=0, offset=(0, 20))
    except:
        pass

    # restore
    #####################
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)


class RSN_OT_DrawNodes(Operator):
    """Draw the active task's settings """
    bl_idname = "rsn.draw_nodes"
    bl_label = "Time Debug"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        try:
            context.area.tag_redraw()
        except AttributeError:  # close windows
            context.scene.RSNBusyDrawing = False
            context.window_manager.event_timer_remove(self._timer)
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}

        if event.type == 'TIMER':
            # show draw
            if context.scene.RSNBusyDrawing:
                if self.alpha < 0.5:
                    self.alpha += 0.02  # show

            # close draw
            else:
                if self.alpha > 0:
                    self.alpha -= 0.02  # fade
                    return {'RUNNING_MODAL'}
                # remove timer / handles
                context.window_manager.event_timer_remove(self._timer)
                bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')

                global curr_draw_timer, curr_draw_handle
                curr_draw_timer = None
                curr_draw_handle = None
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if True in {context.area.type != 'NODE_EDITOR',
                    context.space_data.edit_tree is None,
                    context.space_data.edit_tree.bl_idname not in {'RenderStackNodeTree', 'RenderStackNodeTreeGroup'},
                    context.window_manager.rsn_running_modal}:
            self.report({'WARNING'}, "NodeEditor not found, cannot run operator")
            return {'CANCELLED'}
        # reset draw handle
        global curr_draw_timer, curr_draw_handle
        if curr_draw_timer is not None:
            context.window_manager.event_timer_remove(curr_draw_timer)
            context.scene.RSNBusyDrawing = False
        if curr_draw_handle is not None:
            bpy.types.SpaceNodeEditor.draw_handler_remove(curr_draw_handle, 'WINDOW')
            context.scene.RSNBusyDrawing = False

        # init draw values
        #####################
        pref = get_pref()
        self.alpha = 0
        # text color        # set statue
        ##################
        context.scene.RSNBusyDrawing = True
        # add timer and handles
        self._timer = context.window_manager.event_timer_add(0.01, window=context.window)
        self._handle = bpy.types.SpaceNodeEditor.draw_handler_add(draw_callback_nodeoutline, (self, context),
                                                                  'WINDOW', 'POST_PIXEL')
        curr_draw_timer = self._timer
        curr_draw_handle = self._handle

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.types.Scene.RSNBusyDrawing = BoolProperty(default=False)

    bpy.utils.register_class(RSN_OT_DrawNodes)


def unregister():
    del bpy.types.Scene.RSNBusyDrawing

    bpy.utils.unregister_class(RSN_OT_DrawNodes)
