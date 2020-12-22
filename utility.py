import bpy
from itertools import groupby


class NODE_TREE():
    def __init__(self, node_tree, node_name=None):
        self.nt = node_tree
        self.root_node = node_tree.nodes[node_name] if node_name else node_tree.nodes.active
        self.node_list = self.get_node_list(self.root_node) if node_name else self.get_node_list(self.root_node)
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
                    if sub_node.mute:
                        continue
                    else:
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
        node_list[:] = [node for node in node_list if
                        nt.nodes[node].bl_idname not in ['NodeReroute', 'RSNodeTaskListNode']]
        normal_node_list = [list(g) for k, g in
                            groupby(node_list, lambda name: nt.nodes[name].bl_idname == 'RSNodeTaskNode') if not k]
        task_node_list = [node for node in node_list if nt.nodes[node].bl_idname == 'RSNodeTaskNode']

        for i in range(len(task_node_list)):
            dict[task_node_list[i]] = normal_node_list[i]

        return dict

    def get_task_dict(self, task_name):
        return self.dict[task_name]

    def get_active_node(self):
        return self.nt.nodes.active

    def get_task_data(self, task_name):
        task_data = {}
        for node_name in self.dict[task_name]:
            node = self.nt.nodes[node_name]
            task_data['task_name'] = self.nt.nodes[task_name].task_name
            if node.bl_idname == "RSNodeCamInputNode":
                task_data["camera"] = node.camera.name if node.camera else None

            elif node.bl_idname == "RSNodeResolutionInputNode":
                task_data["res_x"] = node.res_x
                task_data['res_y'] = node.res_y
                task_data['res_scale'] = node.res_scale

            elif node.bl_idname == "RSNodeCyclesRenderSettingsNode":
                task_data['engine'] = "CYCLES"
                task_data['samples'] = node.samples

            elif node.bl_idname == "RSNodeEeveeRenderSettingsNode":
                task_data['engine'] = "BLENDER_EEVEE"
                task_data['samples'] = node.samples

            elif node.bl_idname == "RSNodeWorkBenchRenderSettingsNode":
                task_data['engine'] = 'BLENDER_WORKBENCH'

            elif node.bl_idname == 'RSNodeLuxcoreRenderSettingsNode':
                task_data['engine'] = 'LUXCORE'
                task_data['luxcore_half'] = {'use_samples': node.use_samples,
                                             'samples'    : node.samples,
                                             'use_time'   : node.use_time,
                                             'time'       : node.time}

            elif node.bl_idname == "RSNodeFrameRangeInputNode":
                if node.frame_end < node.frame_start:
                    node.frame_end = node.frame_start
                task_data["frame_start"] = node.frame_start
                task_data["frame_end"] = node.frame_end
                task_data["frame_step"] = node.frame_step

            elif node.bl_idname == "RSNodeImageFormatInputNode":
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

            elif node.bl_idname == 'RSNodeFilePathInputNode':
                task_data['use_blend_file_path'] = node.use_blend_file_path
                task_data['path_format'] = node.path_format
                task_data['path'] = node.path

            elif node.bl_idname == 'RSNodeScriptsNode':
                if node.type == 'SINGLE':
                    if 'scripts' in task_data:
                        task_data['scripts'][node.name] = node.code
                    else:
                        task_data['scripts'] = {node.name: node.code}
                else:
                    if 'scripts_file' in task_data:
                        task_data['scripts_file'][node.name] = node.file.name
                    else:
                        task_data['scripts_file'] = {node.name: node.file.name}

            elif node.bl_idname == 'RSNodeSmtpEmailNode':
                if 'email' in task_data:
                    task_data['email'][node.name] = {'subject'    : node.subject,
                                                     'content'    : node.content,
                                                     'sender_name': node.sender_name,
                                                     'email'      : node.email}
                else:
                    task_data['email'] = {node.name: {'subject'    : node.subject,
                                                      'content'    : node.content,
                                                      'sender_name': node.sender_name,
                                                      'email'      : node.email}}

            elif node.bl_idname == "RSNodeViewLayerInputNode":
                task_data['view_layer'] = node.view_layer

            elif node.bl_idname == "RSNodeLightStudioNode":
                task_data['ssm_light_studio'] = node.light_studio_index

            elif node.bl_idname == "RSNodeWorldInputNode":
                task_data['world'] = node.world.name

            elif node.bl_idname == "RSNodeActiveRenderSlotNode":
                task_data['render_slot'] = node.active_slot_index

            elif node.bl_idname == 'RSNodeObjectMaterialNode':
                if node.object and node.new_material:
                    if 'object_material' in task_data:
                        task_data['object_material'][node.name] = {'object'      : node.object.name,
                                                                   'slot_index'  : node.slot_index,
                                                                   'new_material': node.new_material.name}
                    else:
                        task_data['object_material'] = {node.name: {'object'      : node.object.name,
                                                                    'slot_index'  : node.slot_index,
                                                                    'new_material': node.new_material.name}}
            elif node.bl_idname == 'RSNodeObjectPSRNode':
                if node.object and True in {node.use_p, node.use_s, node.use_r}:
                    if 'object_psr' in task_data:
                        task_data['object_psr'][node.name] = {'object'  : node.object.name,
                                                              'use_p'   : node.use_p,
                                                              'use_s'   : node.use_s,
                                                              'use_r'   : node.use_r,
                                                              'location': node.p,
                                                              'scale'   : node.s,
                                                              'rotation': node.r, }
                    else:
                        task_data['object_psr'] = {node.name: {'object'  : node.object.name,
                                                               'use_p'   : node.use_p,
                                                               'use_s'   : node.use_s,
                                                               'use_r'   : node.use_r,
                                                               'location': node.p,
                                                               'scale'   : node.s,
                                                               'rotation': node.r, }}

            elif node.bl_idname == 'RSNodeViewLayerPassesNode':
                if 'view_layer_passes' in task_data:
                    task_data['view_layer_passes'][node.name] = {'view_layer': node.view_layer,
                                                                 'use_passes': node.use_passes}
                else:
                    task_data['view_layer_passes'] = {node.name: {'view_layer': node.view_layer,
                                                                  'use_passes': node.use_passes}}

            elif node.bl_idname == 'RSNodeColorManagementNode':
                task_data['view_transform'] = node.view_transform
                task_data['look'] = node.look
                task_data['ev'] = node.ev
                task_data['gamma'] = node.gamma

        return task_data
