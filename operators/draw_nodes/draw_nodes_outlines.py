import bpy, blf, bgl
import gpu
from bpy.types import Operator, Panel, Menu
from bpy.props import *
from gpu_extras.batch import batch_for_shader
from math import cos, sin, pi, hypot

from .utils import dpifac, draw_tri_fan, get_node_from_pos
from ...preferences import get_pref


def draw_rounded_node_border(shader, node, radius=8, colour=(1.0, 1.0, 1.0, 0.7)):
    area_width = bpy.context.area.width - (16 * dpifac()) - 1
    bottom_bar = (16 * dpifac()) + 1
    sides = 16
    radius = radius * dpifac()

    nlocx = (node.location.x + 1) * dpifac()
    nlocy = (node.location.y + 1) * dpifac()
    ndimx = node.dimensions.x
    ndimy = node.dimensions.y
    # This is a stupid way to do this...
    if node.parent:
        nlocx += node.parent.location.x
        nlocy += node.parent.location.y
        if node.parent.parent:
            nlocx += node.parent.parent.location.x
            nlocy += node.parent.parent.location.y
            if node.parent.parent.parent:
                nlocx += node.parent.parent.parent.location.x
                nlocy += node.parent.parent.parent.location.y

    if node.hide:
        nlocx += -1
        nlocy += 5
    if node.type == 'REROUTE':
        # nlocx += 1
        nlocy -= 1
        ndimx = 0
        ndimy = 0
        radius += 6

    # Top left corner
    mx, my = bpy.context.region.view2d.view_to_region(nlocx, nlocy, clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (4 <= i <= 8) and my > bottom_bar and mx < area_width:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Top right corner
    mx, my = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy, clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (0 <= i <= 4) and my > bottom_bar and mx < area_width:
            cosine = radius * cos(i * 2 * pi / sides) + mx
            sine = radius * sin(i * 2 * pi / sides) + my
            vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Bottom left corner
    mx, my = bpy.context.region.view2d.view_to_region(nlocx, nlocy - ndimy, clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (8 <= i <= 12):
            if my > bottom_bar and mx < area_width:
                cosine = radius * cos(i * 2 * pi / sides) + mx
                sine = radius * sin(i * 2 * pi / sides) + my
                vertices.append((cosine, sine))

    draw_tri_fan(shader, vertices, colour)

    # Bottom right corner
    mx, my = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy - ndimy, clip=False)
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


def draw_callback_nodeoutline(self, context):
    if context.window_manager.rsn_node_list == '':
        pass

    bgl.glLineWidth(1)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glHint(bgl.GL_LINE_SMOOTH_HINT, bgl.GL_NICEST)

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

    col_outer = (self.color[0], self.color[1], self.color[2], self.alpha)
    col_inner = (0.0, 0.0, 0.0, self.alpha + 0.1)

    node_list = context.window_manager.rsn_node_list.split(',')

    for node_name in node_list:
        try:
            node = context.space_data.edit_tree.nodes[node_name]
            draw_rounded_node_border(shader, node, radius=self.radius, colour=col_outer)  # outline
            draw_rounded_node_border(shader, node, radius=self.radius - 1, colour=col_inner)  # inner
        except KeyError:
            pass

    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)


class RSN_OT_DrawNodes(Operator, ):
    """"""
    bl_idname = "rsn.draw_nodes"
    bl_label = "Draw Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'TIMER':
            # show draw
            if context.scene.RSNBusyDrawing:
                if self.alpha < 0.5: self.alpha += 0.02

            # close draw
            else:
                if self.alpha > 0:
                    self.alpha -= 0.02
                    return {'RUNNING_MODAL'}
                # remove handles
                bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # init draw values
        self.alpha = 0
        self.radius = get_pref().node_viewer.border_radius
        self.color = get_pref().node_viewer.border_color

        if True in {context.area.type != 'NODE_EDITOR',
                    context.space_data.edit_tree is None,
                    context.space_data.edit_tree.bl_idname != 'RenderStackNodeTree'}:
            self.report({'WARNING'}, "NodeEditor not found, cannot run operator")
            return {'CANCELLED'}

        # set statue
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
