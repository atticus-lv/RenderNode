# some code from node_wrangler

import bpy
import gpu
import bgl

from math import cos, sin, pi, hypot

from gpu_extras.batch import batch_for_shader
from mathutils import Vector


def dpifac():
    prefs = bpy.context.preferences.system
    return prefs.dpi * prefs.pixel_size / 72


def draw_tri_fan(shader, vertices, colour):
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
    shader.bind()
    shader.uniform_float("color", colour)
    batch.draw(shader)


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


def store_mouse_cursor(context, event):
    space = context.space_data
    v2d = context.region.view2d
    tree = space.edit_tree

    # convert mouse position to the View2D for later node placement
    if context.region.type == 'WINDOW':
        space.cursor_location_from_region(event.mouse_region_x, event.mouse_region_y)
    else:
        space.cursor_location = tree.view_center


def get_node_from_pos(nodes, context, event):
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
