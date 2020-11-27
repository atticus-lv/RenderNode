bl_info = {
    "name"       : "RenderStack Node",
    "author"     : "Atticus",
    "version"    : (0, 1),
    "blender"    : (2, 90, 0),
    "location"   : "Node Editor",
    "description": "Node based render queue workflow",
    # "doc_url"    : "",
    "category"   : "Render",
}

import bpy


def register():
    from . import auto_reload
    auto_reload.register()


if __name__ == '__main__':
    # try:
    #     nodeitems_utils.unregister_node_categories("CUSTOM_NODES")
    # except:
    #     pass
    # finally:
    #     register()
    register()
