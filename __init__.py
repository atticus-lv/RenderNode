bl_info = {
    "sender_name": "RenderStack Node ",
    "author"     : "Atticus",
    "version"    : (1, 1, 2),
    "blender"    : (2, 92, 0),
    "location"   : "Node Editor > RenderStackNode Editor",
    "description": "Node based render queue workflow",
    'warning'    : "",
    "doc_url"    : "https://github.com/atticus-lv/RenderStackNode/wiki",
    "category"   : "Render",
}

import importlib
import sys
import os
import json
from itertools import groupby
import bpy

# get folder name
__folder_name__ = __name__
__dict__ = {}
dir = os.path.dirname(__file__)

# get all .py file path
py_paths = [os.path.join(root, f) for root, dirs, files in os.walk(dir) for f in files if
            f.endswith('.py') and f != '__init__.py']

for i, path in enumerate(py_paths):
    name = os.path.basename(path)[:-3]
    correct_path = path.replace('\\', '/')
    # split path with folder name
    path_list = [list(g) for k, g in groupby(correct_path.split('/'), lambda x: x == __folder_name__) if
                 not k]
    # combine path and make dict like this: 'name:folder.name'
    if not 'preset' in path_list[-1]:
        r_name_raw = __folder_name__ + '.' + '.'.join(path_list[-1])
        __dict__[name] = r_name_raw[:-3]

# auto reload
for name in __dict__.values():
    if name in sys.modules:
        importlib.reload(sys.modules[name])
    else:
        globals()[name] = importlib.import_module(name)
        setattr(globals()[name], 'modules', __dict__)


def register():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'register'):
            sys.modules[name].register()


def unregister():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'unregister'):
            sys.modules[name].unregister()


if __name__ == '__main__':
    register()
