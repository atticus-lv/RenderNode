import bpy, blf, bgl
import gpu
from bpy.types import Operator, Panel, Menu
from bpy.props import (
    FloatProperty,
    EnumProperty,
    BoolProperty,
    IntProperty,
    StringProperty,
    FloatVectorProperty,
    CollectionProperty,
)
from bpy_extras.io_utils import ImportHelper, ExportHelper
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from math import cos, sin, pi, hypot


def dpifac():
    prefs = bpy.context.preferences.system
    return prefs.dpi * prefs.pixel_size / 72


def store_mouse_cursor(context, event):
    space = context.space_data
    v2d = context.region.view2d
    tree = space.edit_tree

    # convert mouse position to the View2D for later node placement
    if context.region.type == 'WINDOW':
        space.cursor_location_from_region(event.mouse_region_x, event.mouse_region_y)
    else:
        space.cursor_location = tree.view_center


def node_at_pos(nodes, context, event):
    nodes_near_mouse = []
    nodes_under_mouse = []
    target_node = None

    store_mouse_cursor(context, event)
    x, y = context.space_data.cursor_location
    x = x
    y = y

    # Make a list of each corner (and middle of border) for each node.
    # Will be sorted to find nearest point and thus nearest node
    node_points_with_dist = []

    for node in nodes:
        skipnode = False
        if node.type != 'FRAME':  # no point trying to link to a frame node
            locx = node.location.x
            locy = node.location.y
            dimx = node.dimensions.x / dpifac()
            dimy = node.dimensions.y / dpifac()
            if node.parent:
                locx += node.parent.location.x
                locy += node.parent.location.y
                if node.parent.parent:
                    locx += node.parent.parent.location.x
                    locy += node.parent.parent.location.y
                    if node.parent.parent.parent:
                        locx += node.parent.parent.parent.location.x
                        locy += node.parent.parent.parent.location.y
                        if node.parent.parent.parent.parent:
                            # Support three levels or parenting
                            # There's got to be a better way to do this...
                            skipnode = True
            if not skipnode:
                node_points_with_dist.append([node, hypot(x - locx, y - locy)])  # Top Left
                node_points_with_dist.append([node, hypot(x - (locx + dimx), y - locy)])  # Top Right
                node_points_with_dist.append([node, hypot(x - locx, y - (locy - dimy))])  # Bottom Left
                node_points_with_dist.append([node, hypot(x - (locx + dimx), y - (locy - dimy))])  # Bottom Right

                node_points_with_dist.append([node, hypot(x - (locx + (dimx / 2)), y - locy)])  # Mid Top
                node_points_with_dist.append([node, hypot(x - (locx + (dimx / 2)), y - (locy - dimy))])  # Mid Bottom
                node_points_with_dist.append([node, hypot(x - locx, y - (locy - (dimy / 2)))])  # Mid Left
                node_points_with_dist.append([node, hypot(x - (locx + dimx), y - (locy - (dimy / 2)))])  # Mid Right

    nearest_node = sorted(node_points_with_dist, key=lambda k: k[1])[0][0]

    for node in nodes:
        if node.type != 'FRAME' and not skipnode:
            locx = node.location.x
            locy = node.location.y
            dimx = node.dimensions.x / dpifac()
            dimy = node.dimensions.y / dpifac()
            if node.parent:
                locx += node.parent.location.x
                locy += node.parent.location.y
            if (locx <= x <= locx + dimx) and \
                    (locy - dimy <= y <= locy):
                nodes_under_mouse.append(node)

    if len(nodes_under_mouse) == 1:
        if nodes_under_mouse[0] != nearest_node:
            target_node = nodes_under_mouse[0]  # use the node under the mouse if there is one and only one
        else:
            target_node = nearest_node  # else use the nearest node
    else:
        target_node = nearest_node
    return target_node


def draw_line(x1, y1, x2, y2, size, colour=(1.0, 1.0, 1.0, 0.7)):
    shader = gpu.shader.from_builtin('2D_SMOOTH_COLOR')

    vertices = ((x1, y1), (x2, y2))
    vertex_colors = ((colour[0] + (1.0 - colour[0]) / 4,
                      colour[1] + (1.0 - colour[1]) / 4,
                      colour[2] + (1.0 - colour[2]) / 4,
                      colour[3] + (1.0 - colour[3]) / 4),
                     colour)

    batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": vertices, "color": vertex_colors})
    bgl.glLineWidth(size * dpifac())

    shader.bind()
    batch.draw(shader)


def draw_circle_2d_filled(shader, mx, my, radius, colour=(1.0, 1.0, 1.0, 0.7)):
    radius = radius * dpifac()
    sides = 12
    vertices = [(radius * cos(i * 2 * pi / sides) + mx,
                 radius * sin(i * 2 * pi / sides) + my)
                for i in range(sides + 1)]

    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
    shader.bind()
    shader.uniform_float("color", colour)
    batch.draw(shader)


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
        if (4 <= i <= 8):
            if my > bottom_bar and mx < area_width:
                cosine = radius * cos(i * 2 * pi / sides) + mx
                sine = radius * sin(i * 2 * pi / sides) + my
                vertices.append((cosine, sine))
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
    shader.bind()
    shader.uniform_float("color", colour)
    batch.draw(shader)

    # Top right corner
    mx, my = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy, clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (0 <= i <= 4):
            if my > bottom_bar and mx < area_width:
                cosine = radius * cos(i * 2 * pi / sides) + mx
                sine = radius * sin(i * 2 * pi / sides) + my
                vertices.append((cosine, sine))
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
    shader.bind()
    shader.uniform_float("color", colour)
    batch.draw(shader)

    # Bottom left corner
    mx, my = bpy.context.region.view2d.view_to_region(nlocx, nlocy - ndimy, clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (8 <= i <= 12):
            if my > bottom_bar and mx < area_width:
                cosine = radius * cos(i * 2 * pi / sides) + mx
                sine = radius * sin(i * 2 * pi / sides) + my
                vertices.append((cosine, sine))
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
    shader.bind()
    shader.uniform_float("color", colour)
    batch.draw(shader)

    # Bottom right corner
    mx, my = bpy.context.region.view2d.view_to_region(nlocx + ndimx, nlocy - ndimy, clip=False)
    vertices = [(mx, my)]
    for i in range(sides + 1):
        if (12 <= i <= 16):
            if my > bottom_bar and mx < area_width:
                cosine = radius * cos(i * 2 * pi / sides) + mx
                sine = radius * sin(i * 2 * pi / sides) + my
                vertices.append((cosine, sine))
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
    shader.bind()
    shader.uniform_float("color", colour)
    batch.draw(shader)

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
    if context.window_manager.rsn_node_list != '':

        bgl.glLineWidth(1)
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glHint(bgl.GL_LINE_SMOOTH_HINT, bgl.GL_NICEST)

        nodes, links = get_nodes_links(context)

        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

        col_outer = (0.2, 1.0, 0.2, self.alpha)
        col_inner = (0.0, 0.0, 0.0, self.alpha + 0.1)

        node_list = context.window_manager.rsn_node_list.split(',')

        for node_name in node_list:
            node = context.space_data.edit_tree.nodes[node_name]

            draw_rounded_node_border(shader, node, radius=6, colour=col_outer)  # outline
            draw_rounded_node_border(shader, node, radius=5, colour=col_inner)  # inner

        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_LINE_SMOOTH)


def get_active_tree(context):
    tree = context.space_data.node_tree
    path = []
    # Get nodes from currently edited tree.
    # If user is editing a group, space_data.node_tree is still the base level (outside group).
    # context.active_node is in the group though, so if space_data.node_tree.nodes.active is not
    # the same as context.active_node, the user is in a group.
    # Check recursively until we find the real active node_tree:
    if tree.nodes.active:
        while tree.nodes.active != context.active_node:
            tree = tree.nodes.active.node_tree
            path.append(tree)
    return tree, path


def get_nodes_links(context):
    tree, path = get_active_tree(context)
    return tree.nodes, tree.links


class RSNBase:
    @classmethod
    def poll(cls, context):
        return context.space.type == 'NODE_EDITOR' and context.space.node_tree and context.space.tree_type == 'RenderStackNodeTree'


class RSN_OT_DrawNodes(Operator, RSNBase):
    """Add a Mix RGB/Shader node by interactively drawing lines between nodes"""
    bl_idname = "rsn.draw_nodes"
    bl_label = "Draw Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        context.area.tag_redraw()
        node_list = bpy.context.window_manager.rsn_node_list.split(',')
        nodes = [context.space_data.edit_tree.nodes[name] for name in node_list]
        cont = True

        start_pos = [event.mouse_region_x, event.mouse_region_y]

        if event.type == 'MOUSEMOVE':
            return {'PASS_THROUGH'}

        elif event.type == 'RIGHTMOUSE' and event.value == 'RELEASE':
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')

            return {'FINISHED'}

        elif event.type == 'ESC':
            print('cancelled')
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        elif event.type == 'TIMER':
            print(self.time_count)
            if self.time_count > 0:
                self.time_count -= 1
                self.alpha -= 0.005
                return {'RUNNING_MODAL'}
            else:
                bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
                return {'FINISHED'}

        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.time_count = 100
        self.alpha = 0.5
        if context.area.type == 'NODE_EDITOR':
            # the arguments we pass the the callback
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'

            self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            self._handle = bpy.types.SpaceNodeEditor.draw_handler_add(draw_callback_nodeoutline, (self, context),
                                                                      'WINDOW',
                                                                      'POST_PIXEL')

            print("INVOKE")
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


classes = (
    RSN_OT_DrawNodes,

)


def register():
    from bpy.utils import register_class

    # props
    bpy.types.Scene.RSNBusyDrawing = StringProperty(
        name="Busy Drawing!",
        default="",
        description="An internal property used to store only the first mouse position")
    bpy.types.Scene.RSNLazySource = StringProperty(
        name="Lazy Source!",
        default="x",
        description="An internal property used to store the first node in a Lazy Connect operation")
    bpy.types.Scene.RSNLazyTarget = StringProperty(
        name="Lazy Target!",
        default="x",
        description="An internal property used to store the last node in a Lazy Connect operation")

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    # props
    del bpy.types.Scene.RSNBusyDrawing
    del bpy.types.Scene.RSNLazySource
    del bpy.types.Scene.RSNLazyTarget

    for cls in classes:
        unregister_class(cls)
