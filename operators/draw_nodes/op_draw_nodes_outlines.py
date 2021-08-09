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
from ...nodes.BASE._runtime import cache_node_times, cache_node_dependants
from ...nodes.BASE.node_base import cache_executed_nodes


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

    # # if node have parent
    # loc = find_node_parent(node).location
    # nlocx += loc.x
    # nlocy += loc.y

    return nlocx, nlocy, ndimx, ndimy


def get_node_vertices(nlocx, nlocy, ndimx, ndimy):
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


def draw_text_on_node(color, text, node, size=15, corner_index=1):
    '''index 0,1,2,3: top_left, top_right, bottom_left, bottom_right'''
    nlocx, nlocy, ndimx, ndimy = get_node_location(node)
    corners = get_node_vertices(nlocx, nlocy, ndimx, ndimy)
    pos = corners[corner_index]

    loc_x, loc_y = bpy.context.region.view2d.view_to_region(pos[0], pos[1], clip=False)
    draw_text_2d(color, text, loc_x, loc_y, size)


def draw_round_rectangle(shader, points, radius=8, colour=(1.0, 1.0, 1.0, 0.7)):
    sides = 16
    radius = 16

    # fill
    draw_tri_fan(shader, points, colour)

    top_left = points[1]
    top_right = points[0]
    bottom_left = points[2]
    bottom_right = points[3]

    # Top edge
    top_left_top = (top_left[0], top_left[1] + radius)
    top_right_top = (top_right[0], top_right[1] + radius)
    vertices = [top_right_top, top_left_top, top_left, top_right]
    draw_tri_fan(shader, vertices, colour)

    # Left edge
    top_left_left = (top_left[0] - radius, top_left[1])
    bottom_left_left = (bottom_left[0] - radius, bottom_left[1])
    vertices = [top_left, top_left_left, bottom_left_left, bottom_left]
    draw_tri_fan(shader, vertices, colour)

    # Bottom edge
    bottom_left_bottom = (bottom_left[0], bottom_left[1] - radius)
    bottom_right_bottom = (bottom_right[0], bottom_right[1] - radius)
    vertices = [bottom_right, bottom_left, bottom_left_bottom, bottom_right_bottom]
    draw_tri_fan(shader, vertices, colour)

    # right edge
    top_right_right = (top_right[0] + radius, top_right[1])
    bottom_right_right = (bottom_right[0] + radius, bottom_right[1])
    vertices = [top_right_right, top_right, bottom_right, bottom_right_right]
    draw_tri_fan(shader, vertices, colour)

    # Top right corner
    vertices = [top_right]
    mx = top_right[0]
    my = top_right[1]
    for i in range(sides + 1):
        if 0 <= i <= 4:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Top left corner
    vertices = [top_left]
    mx = top_left[0]
    my = top_left[1]
    for i in range(sides + 1):
        if 4 <= i <= 8:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Bottom left corner
    vertices = [bottom_left]
    mx = bottom_left[0]
    my = bottom_left[1]
    for i in range(sides + 1):
        if 8 <= i <= 12:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Bottom right corner
    vertices = [bottom_right]
    mx = bottom_right[0]
    my = bottom_right[1]
    for i in range(sides + 1):
        if 12 <= i <= 16:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)


def draw_rounded_node_border(shader, node, radius=8, colour=(1.0, 1.0, 1.0, 0.7)):
    area_width = bpy.context.area.width - (16 * dpifac()) - 1
    bottom_bar = (16 * dpifac()) + 1
    sides = 16
    radius = radius * dpifac()

    nlocx, nlocy, ndimx, ndimy = get_node_location(node)

    if node.hide:
        nlocx += -1
        nlocy += 5
    if node.type == 'REROUTE':
        # nlocx += 1
        nlocy -= 1
        ndimx = 0
        ndimy = 0
        radius += 6

    top_left, top_right, bottom_left, bottom_right = get_node_vertices(nlocx, nlocy, ndimx, ndimy)

    # Top left corner
    mx, my = bpy.context.region.view2d.view_to_region(top_left[0], top_left[1], clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (4 <= i <= 8) and my > bottom_bar and mx < area_width:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Top right corner
    mx, my = bpy.context.region.view2d.view_to_region(top_right[0], top_right[1], clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (0 <= i <= 4) and my > bottom_bar and mx < area_width:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Bottom left corner
    mx, my = bpy.context.region.view2d.view_to_region(bottom_left[0], bottom_left[1], clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if 8 <= i <= 12:
            if my > bottom_bar and mx < area_width:
                cosine = radius * cos(i * 2 * pi / sides) + mx
                sine = radius * sin(i * 2 * pi / sides) + my
                vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Bottom right corner
    mx, my = bpy.context.region.view2d.view_to_region(bottom_right[0], bottom_right[1], clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (12 <= i <= 16) and my > bottom_bar and mx < area_width:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # prepare drawing all edges in one batch
    vertices = []
    indices = []
    id_last = 0

    # Left edge
    m1x, m1y = bpy.context.region.view2d.view_to_region(nlocx, nlocy, clip=False)
    m2x, m2y = bpy.context.region.view2d.view_to_region(nlocx, nlocy - ndimy, clip=False)
    if m1x < area_width and m2x < area_width:
        vertices.extend([(m2x - radius, m2y), (m2x, m2y),
                         (m1x, m1y), (m1x - radius, m1y)])
        indices.extend([(id_last, id_last + 1, id_last + 3),
                        (id_last + 3, id_last + 1, id_last + 2)])
        id_last += 4

    # Top edge
    m1x, m1y = bpy.context.region.view2d.view_to_region(nlocx, nlocy, clip=False)
    m2x, m2y = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy, clip=False)
    m1x = min(m1x, area_width)
    m2x = min(m2x, area_width)
    if m1y > bottom_bar and m2y > bottom_bar:
        vertices.extend([(m1x, m1y), (m2x, m1y),
                         (m2x, m1y + radius), (m1x, m1y + radius)])
        indices.extend([(id_last, id_last + 1, id_last + 3),
                        (id_last + 3, id_last + 1, id_last + 2)])
        id_last += 4

    # Right edge
    m1x, m1y = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy, clip=False)
    m2x, m2y = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy - ndimy, clip=False)
    m1y = max(m1y, bottom_bar)
    m2y = max(m2y, bottom_bar)
    if m1x < area_width and m2x < area_width:
        vertices.extend([(m1x, m2y), (m1x + radius, m2y),
                         (m1x + radius, m1y), (m1x, m1y)])
        indices.extend([(id_last, id_last + 1, id_last + 3),
                        (id_last + 3, id_last + 1, id_last + 2)])
        id_last += 4

    # Bottom edge
    m1x, m1y = bpy.context.region.view2d.view_to_region(nlocx, nlocy - ndimy, clip=False)
    m2x, m2y = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy - ndimy, clip=False)
    m1x = min(m1x, area_width)
    m2x = min(m2x, area_width)
    if m1y > bottom_bar and m2y > bottom_bar:
        vertices.extend([(m1x, m2y), (m2x, m2y),
                         (m2x, m1y - radius), (m1x, m1y - radius)])
        indices.extend([(id_last, id_last + 1, id_last + 3),
                        (id_last + 3, id_last + 1, id_last + 2)])

    # now draw all edges in one batch
    if len(vertices) != 0:
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
        shader.bind()
        shader.uniform_float("color", colour)
        batch.draw(shader)


# TODO make draw outline when executing
def draw_callback_nodeoutline(self, context):
    if context.window_manager.rsn_viewer_node == '':
        pass

    bgl.glLineWidth(1)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glHint(bgl.GL_LINE_SMOOTH_HINT, bgl.GL_NICEST)

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

    # draw outline
    ########################
    # set color
    white = (1, 1, 1, 1)
    orange = (0, 1, 0, 1)
    red = (1, 0, 0, 1)

    task_outer = (self.task_color[0], self.task_color[1], self.task_color[2], self.alpha)
    col_outer = (self.settings_color[0], self.settings_color[1], self.settings_color[2], self.alpha)
    col_inner = (0.0, 0.0, 0.0, self.alpha + 0.1)

    task_node = context.space_data.edit_tree.nodes.get(context.window_manager.rsn_viewer_node)
    if not task_node: return

    node_list = [node for node in context.space_data.edit_tree.nodes if node in cache_executed_nodes]
    for node in node_list:
        if node == task_node:
            draw_rounded_node_border(shader, task_node, radius=self.radius * 1.25, colour=task_outer)
            draw_rounded_node_border(shader, task_node, radius=self.radius * 1.25 - 1.25, colour=col_inner)
        else:
            draw_rounded_node_border(shader, node, radius=self.radius, colour=col_outer)
            draw_rounded_node_border(shader, node, radius=self.radius - 1, colour=col_inner)
        # draw time
        if node.id_data in cache_node_times:
            if node in cache_node_times[node.id_data]:
                times = cache_node_times[node.id_data][node]
                t = times['Execution'] if node.bl_idname != 'RenderNodeGroup' else times['Group']
                if t < 0.01:
                    col = white
                elif t < 0.1:
                    col = orange
                else:
                    col = red
                draw_text_on_node(col, f"{t:.2f} ns", node, size=15, corner_index=0)


    # draw text
    ##################
    # if self.show_text_info:
    #     # properties text
    #     task_text = "No Active Task!" if context.window_manager.rsn_viewer_node == '' else context.window_manager.rsn_viewer_node
    #     camera = context.scene.camera.name if context.scene.camera else "No Scene camera"
    #     is_save = True if bpy.data.filepath != '' else False
    #     file_path_text = context.scene.render.filepath if is_save else "Save your file first!"
    #
    #     texts = [
    #         f"Task: {task_text}",
    #         f"Camera: {camera}",
    #         f"Engine: {context.scene.render.engine}",
    #         f"Frame: {context.scene.frame_start} - {context.scene.frame_end}",
    #         f"FilePath: {file_path_text}",
    #     ]
    #
    #     # text background
    #     r, g, b = self.background_color
    #     longest_text = max(texts, key=len, default='')
    #     size = blf.dimensions(0, longest_text)  # get the longest text
    #     size = [v * 1.5 / context.preferences.view.ui_scale for v in size]  # scale with the ui scale
    #
    #     # set corner
    #     top = 125
    #     bottom = 25
    #     step = 25
    #
    #     vertices = [(10 + size[0], top + size[1]), (20, top + size[1]), (20, 25), (10 + size[0], bottom), ]
    #
    #     draw_round_rectangle(shader, vertices, radius=18, colour=(0, 0, 0, self.alpha))  # shadow
    #     draw_round_rectangle(shader, vertices, radius=14, colour=(r, g, b, self.alpha))  # main box
    #
    #     # draw texts
    #     r, g, b = self.text_color
    #     size = 20
    #
    #     for i, text in enumerate(texts):
    #         draw_text_2d((r, g, b, self.alpha, size), text, 20, top - step * i)
    # restore
    #####################
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)

class RSN_OT_DrawNodes(Operator):
    """Draw the active task's settings """
    bl_idname = "rsn.draw_nodes"
    bl_label = "Draw Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'TIMER':
            # show draw
            if context.scene.RSNBusyDrawing:
                if self.alpha < 0.5: self.alpha += 0.02  # show

            # close draw
            else:
                if self.alpha > 0:
                    self.alpha -= 0.02  # fade
                    return {'RUNNING_MODAL'}
                # remove timer / handles
                context.window_manager.event_timer_remove(self._timer)
                bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if True in {context.area.type != 'NODE_EDITOR',
                    context.space_data.edit_tree is None,
                    context.space_data.edit_tree.bl_idname != 'RenderStackNodeTree'}:
            self.report({'WARNING'}, "NodeEditor not found, cannot run operator")
            return {'CANCELLED'}

        # init draw values
        #####################
        pref = get_pref()
        self.alpha = 0
        self.radius = pref.draw_nodes.border_radius
        # node color
        self.settings_color = pref.draw_nodes.settings_color
        self.task_color = pref.draw_nodes.task_color
        self.file_path_color = pref.draw_nodes.file_path_color

        self.show_text_info = pref.draw_nodes.show_text_info
        # background color
        self.background_color = pref.draw_nodes.background_color
        # text color
        self.text_color = pref.draw_nodes.text_color
        # set statue
        ##################
        context.scene.RSNBusyDrawing = True
        # add timer and handles
        self._timer = context.window_manager.event_timer_add(0.01, window=context.window)
        self._handle = bpy.types.SpaceNodeEditor.draw_handler_add(draw_callback_nodeoutline, (self, context),
                                                                  'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.types.Scene.RSNBusyDrawing = BoolProperty(default=False)

    bpy.utils.register_class(RSN_OT_DrawNodes)


def unregister():
    del bpy.types.Scene.RSNBusyDrawing

    bpy.utils.unregister_class(RSN_OT_DrawNodes)
