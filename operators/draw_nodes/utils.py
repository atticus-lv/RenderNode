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
