import argparse
import bpy
import sys


def main(args):
    print("Script args: ", args)

    if len(args) > 0:
        parser = argparse.ArgumentParser()
        parser.add_argument('blend')
        parser.add_argument('--pack', action='append')
        args = parser.parse_args(args)

        blend = args.blend

        print(f"Blend to fix: {blend}")

        bpy.ops.wm.open_mainfile(filepath=blend)

        ###
        node = bpy.data.node_groups['NodeTree'].nodes['Task Render List']
        node.is_active_list = True

        if hasattr(node, 'active_index'):
            try:
                setattr(node, 'active_index', 1)
            except Exception as e:
                print(e)
        ###

        bpy.context.view_layer.update()


if __name__ == "__main__":
    if "--" not in sys.argv:
        argv = []  # as if no args are passed
    else:
        argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"
    main(argv)
