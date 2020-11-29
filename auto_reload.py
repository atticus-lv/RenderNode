import os
import json

directory = os.path.dirname(__file__)
parent_dir = os.path.basename(directory)


def path_to_dict(path, my_string=None):
    name = os.path.basename(path)
    if name in ['__pycache__', '.git', '.idea', 'img', '__init__.py']:
        return None
    if os.path.isdir(path):
        d = {name: []}
        paths = [os.path.join(path, x) for x in os.listdir(path)]
        for p in paths:
            c = path_to_dict(p, my_string)
            if c is not None:
                d[name].append(c)
        if not d[name]:
            return None
    elif name.endswith('.py'):
        d = name
    else:
        return None

    return d


a = path_to_dict(directory)

print(filenames)
