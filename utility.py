import bpy
from itertools import groupby


class NODE_TREE():
    def __init__(self, node_tree):
        self.nt = node_tree
        self.node_list = self.get_node_list(node_tree.nodes.active)
        self.dict = self.separate_nodes(self.node_list)

    def get_node_list(self, node):
        node_list = []

        def get_node(node):
            if len(node_list) == 0 or (node.name != node_list[-1] and len(node_list) != 0):
                node_list.append(node.name)

        def get_sub_node(node):
            for input in node.inputs:
                if input.is_linked:
                    sub_node = input.links[0].from_node
                    get_sub_node(sub_node)
                else:
                    continue
            # get node itself after get all input nodes
            get_node(node)

        get_sub_node(node)

        return node_list

    def separate_nodes(self, node_list):
        dict = {}
        nt = bpy.context.space_data.edit_tree
        node_list[:] = [node for node in node_list if nt.nodes[node].bl_idname != 'NodeReroute']
        normal_node_list = [list(g) for k, g in
                            groupby(node_list, lambda name: nt.nodes[name].bl_idname == 'RSNodeTaskNode') if not k]
        task_node_list = [node for node in node_list if nt.nodes[node].bl_idname == 'RSNodeTaskNode']

        for i in range(len(task_node_list)):
            dict[task_node_list[i]] = normal_node_list[i]

        return dict

    def get_task_dict(self, task_name):
        return self.dict[task_name]

    def get_task_data(self, task_name):
        task_data = {}
        for node_name in self.dict[task_name]:
            node = self.nt.nodes[node_name]

            if node.bl_idname == "RSNodeCamInputNode":
                task_data["camera"] = node.camera.name if node.camera else None

            elif node.bl_idname == "ResolutionInputNode":
                task_data["res_x"] = node.res_x
                task_data['res_y'] = node.res_y
                task_data['res_scale'] = node.res_scale

            elif node.bl_idname == "RSNodeCyclesRenderSettingsNode":
                task_data['engine'] = "CYCLES"
                task_data['samples'] = node.inputs["Samples"].default_value

            elif node.bl_idname == "RSNodeEeveeRenderSettingsNode":
                task_data['engine'] = "BLENDER_EEVEE"
                task_data['samples'] = node.inputs["Samples"].default_value

            elif node.bl_idname == "FrameRangeInputNode":
                if node.frame_end < node.frame_start:
                    node.frame_end = node.frame_start
                task_data["frame_start"] = node.frame_start
                task_data["frame_end"] = node.frame_end
                task_data["frame_step"] = node.frame_step

            elif node.bl_idname == "ImageFormatInputNode":
                if node.file_format == "JPEG":
                    if node.color_mode == "RGBA":
                        node.color_mode = "RGB"
                    if node.color_depth in ("16", "32"):
                        node.color_depth = "8"

                elif node.file_format == "PNG":
                    if node.color_depth == '32':
                        node.color_depth = "16"

                elif node.file_format == "OPEN_EXR_MULTILAYER":
                    if node.color_depth == "8":
                        node.color_depth = "16"

                task_data['color_mode'] = node.color_mode
                task_data['color_depth'] = node.color_depth
                task_data['file_format'] = node.file_format
                task_data['transparent'] = node.transparent

            elif node.bl_idname == 'FilePathInputNode':
                task_data['use_blend_file_path'] = node.use_blend_file_path
                task_data['path_format'] = node.path_format
                task_data['path'] = node.path

        return task_data