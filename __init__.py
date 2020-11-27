bl_info = {
    "name"       : "RenderStack Node",
    "author"     : "Atticus",
    "version"    : (0, 3),
    "blender"    : (2, 90, 0),
    "location"   : "Node Editor",
    "description": "Node based render queue workflow",
    # "doc_url"    : "",
    "category"   : "Render",
}

import bpy
from . import auto_reload


def register():
    auto_reload.register()


def unregister():
    auto_reload.unregister()


if __name__ == '__main__':
    register()
