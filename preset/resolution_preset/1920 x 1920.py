import bpy
nt = bpy.context.space_data.edit_tree
node = nt.nodes.active
node.res_x = 1920
node.res_y = 1920
node.res_scale = 100
