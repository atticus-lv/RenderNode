import os
import importlib
import sys

from RenderStackNode.node_tree import RenderStackNode
from RenderStackNode import nodes
from RenderStackNode import node_tree

__dict__ = {}
__dict__["node_tree"] = "RenderStackNode.node_tree"

a = nodes.a
for k, v in a.items():
    for module_name in v:
        __dict__[module_name] = f"RenderStackNode.nodes.{k}.{module_name}"

# print(__dict__)

for full_name in __dict__.values():
    if full_name in sys.modules:
        importlib.reload(sys.modules[full_name])
    else:
        globals()[full_name] = importlib.import_module(full_name)
        setattr(globals()[full_name], 'modules', __dict__)


def register():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'register'):
            try:
                sys.modules[name].register()
            except Exception as e:
                print(f"{name} register failed: {e}")


def unregister():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'unregister'):
            try:
                sys.modules[name].unregister()
            except Exception as e:
                print(f"{name} unregister failed: {e}")
