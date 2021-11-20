import json

import bpy

from bpy.props import *
from mathutils import Color, Vector

from ._runtime import cache_node_dependants, cache_socket_links, cache_socket_variables, cache_node_group_outputs, \
    runtime_info, logger, MeasureTime, cache_executed_nodes
import uuid


# some method comes from rigging_nodes
class RenderNodeBase(bpy.types.Node):
    bl_label = "RenderStack Node"

    last_ex_id: StringProperty()

    warning: BoolProperty(name='Is warning', default=False)
    warning_msg: StringProperty(name='warning message', default='')

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'RenderStackNodeTree', 'RenderStackNodeTreeGroup'}

    ## BASE METHOD
    #########################################

    def copy(self, node):
        if self.bl_idname in {'RenderNodeTask', 'RSNodeTaskNode'}: self.label = self.name
        if hasattr(self, 'is_active_task'): self.is_active_task = False
        print(f"RSN Copied {self.name} from {node.name}")

    def free(self):
        """Remove Node"""
        print("RSN removed node", self.name)

    ## INITIAL METHOD
    #########################################

    # behaviors = [
    #     ('NONE', 'None', '')
    # ]
    #
    # ip_sockets = {
    #     'name': {
    #         'type': None,
    #         'behaviors': None,
    #         'text': None,
    #     }
    # }
    #
    # op_sockets = {
    #     'name': {
    #         'behaviors': None,
    #         'type': None,
    #         'text': None,
    #     }
    # }
    #
    # def update_sockets(self):
    #     for name, info in self.ip_sockets.items():
    #         if info['type'] == None or not hasattr(self,'operate_type'): continue
    #         if self.operate_type in info['behaviors']:
    #             self.create_input(info['type'], name, info['text'])
    #         else:
    #             self.remove_input(name)
    #
    #     for name, info in self.op_sockets.items():
    #         if info['type'] == None or not hasattr(self,'operate_type'): continue
    #         if self.operate_type in info['behaviors']:
    #             self.create_output(info['type'], name, info['text'])
    #         else:
    #             self.remove_output(name)

    def create_input(self, socket_type, socket_name, socket_label, default_value=None, show_text=True):
        if self.inputs.get(socket_name):
            input = self.inputs[socket_name]
            if hasattr(input, 'text') and input.text != socket_label:
                input.text = socket_label
                input.show_text = show_text
            return None

        input = self.inputs.new(socket_type, socket_name)
        if hasattr(input, 'text'): input.text = socket_label

        if default_value: input.default_value = default_value
        if hasattr(input, 'shape'): input.change_shape()

        return input

    def remove_input(self, socket_name):
        input = self.inputs.get(socket_name)
        if input:
            self.inputs.remove(input)

    def create_output(self, socket_type, socket_name, socket_label, default_value=None, show_text=True):
        if self.outputs.get(socket_name):
            return None

        output = self.outputs.new(socket_type, socket_name)
        if hasattr(output, 'text'):
            output.text = socket_label
            output.show_text = show_text

        if default_value: output.default_value = default_value
        if hasattr(output, 'shape'): output.change_shape()

        return output

    def remove_output(self, socket_name):
        output = self.outputs.get(socket_name)
        if output:
            self.outputs.remove(output)

    def show_input(self, name, show=True):
        input = self.inputs.get(name)
        if input is None: return
        input.hide = False if not show else True

    def show_output(self, name, show=True):
        output = self.outputs.get(name)
        if output is None: return
        output.hide = False if not show else True

    ## STATE METHOD
    #########################################

    def draw_buttons(self, context, layout):
        if self.warning is True:
            msg = layout.operator('rsn.show_task_details', icon='ERROR', text='Show Waring Message')
            msg.task_data = self.warning_msg

    def set_warning(self, msg=''):
        self.warning_msg = msg

        self.use_custom_color = 1
        self.color = (1, 0, 0)
        self.warning = True

        logger.warning(f'{self.name}')

    ## UPDATE METHOD
    #########################################

    def get_dependant_nodes(self):
        '''returns the nodes connected to the inputs of this node'''
        dep_tree = cache_node_dependants.setdefault(self.id_data, {})

        # if self.bl_idname != 'RSNodeSetVariantsNode':

        if self in dep_tree:
            return dep_tree[self]
        nodes = []
        for input in self.inputs:
            connected_socket = input.connected_socket
            if connected_socket and connected_socket not in nodes:
                nodes.append(connected_socket.node)
        dep_tree[self] = nodes

        return nodes

    def execute_dependants(self, context, id, path):
        '''Responsible of executing the required nodes for the current node to work'''
        for x in self.get_dependant_nodes():
            self.execute_other(context, id, path, x)

    def execute(self, context, id, path):
        if self.last_ex_id == id or self.mute: return

        self.last_ex_id = id

        with MeasureTime(self, 'Dependants'):
            self.execute_dependants(context, id, path)
        with MeasureTime(self, 'Group'):
            self.process_group(context, id, path)
            if self not in cache_executed_nodes: cache_executed_nodes.append(self)
        with MeasureTime(self, 'Execution'):
            self.process(context, id, path)
            if self not in cache_executed_nodes: cache_executed_nodes.append(self)

        # if self.bl_idname == 'RSNodeVariantsNode':
        #     self.execute_dependants(context, id, path)

        logger.debug(f'Execute: <{self.name}>')

    def path_to_node(self, path):
        node_tree = bpy.data.node_groups.get(path[0])
        for x in path[1:-1]:
            node_tree = node_tree.nodes.get(x).node_tree
        node = node_tree.nodes.get(path[-1])
        return node

    def execute_other(self, context, id, path, other):
        if hasattr(other, 'execute'):
            other.execute(context, id, path)
        else:
            if other.bl_rna.identifier == 'NodeGroupInput':
                if len(path) < 2:
                    raise ValueError(f'trying to setup the values of a nodegroup input on the upper level')
                node = self.path_to_node(path)
                assert node, f'{path} cannot be resolved to a node'
                for i, output in enumerate(other.outputs):
                    if output.bl_rna.identifier != 'NodeSocketVirtual':
                        if self.id_data.bl_idname == 'RenderStackNodeTreeGroup':
                            other_socket = node.inputs[i]
                            output.set_value(other_socket.get_value())

            elif other.bl_rna.identifier == 'NodeGroupOutput':
                nodes = set()
                for input in other.inputs:
                    if input.bl_rna.identifier != 'NodeSocketVirtual':
                        connected_socket = input.connected_socket

                        if connected_socket and connected_socket not in nodes:
                            node = connected_socket.node
                            self.execute_other(context, id, path, node)
                            nodes.add(node)

    def update(self):
        if runtime_info['executing'] is True:
            return

        # for input in self.inputs:
        #     input.remove_incorrect_links()

    def auto_update_inputs(self, socket_type='RSNodeSocketTaskSettings', socket_name='Input', start_update_index=0):
        """add or remove inputs automatically
        :parm socket_type: any socket type that is registered in blender
        :parm socket_name: custom name for the socket
        """
        count = 0
        for index, input in enumerate(self.inputs):
            if index < start_update_index: continue
            if not input.is_linked and input.bl_idname == socket_type:
                # keep at least one input for links with py commands
                if count == 0:
                    count += 1
                elif input.bl_idname == socket_type:
                    self.inputs.remove(input)
        # auto add inputs
        if count == 0:
            input = self.inputs.new(socket_type, socket_name)
            if hasattr(input, 'shape'): input.display_shape = input.shape

    ## RSN DATA MANAGE
    #########################################

    # update the build-in values with update the hole tree
    def execute_tree(self):
        cache_executed_nodes.clear()
        self.id_data.execute(bpy.context)

    def get_input_value(self, socket_name):
        ans = self.inputs.get(socket_name)
        if ans: return ans.get_value()

    def process_task(self, index=None, set=True):
        if index is not None and index < len(self.inputs):
            task = self.inputs[index]
        else:
            task = self.inputs.get('task')
        value = None
        if task:
            value = task.get_value()
            output = self.outputs.get('task')
            if output and set: output.set_value(value)
            return value

    def task_dict_append(self, info: dict):
        value_pre = self.process_task(set=False)
        if value_pre is None: return

        data = json.loads(value_pre)
        data.update(info)
        output = self.outputs.get('task')
        value_post = json.dumps(data)
        if output and set: output.set_value(value_post)

    def process(self, context, id, path):
        pass

    def process_group(self, context, id, path):
        pass

    ### old method ###
    def get_data(self):
        """For get self date into rsn tree method"""
        pass

    ## Utility
    #########################################
    @staticmethod
    def compare(obj: object, attr: str, val):
        """Use for compare and apply attribute since some properties change may cause depsgraph changes"""
        try:
            if getattr(obj, attr) != val:
                setattr(obj, attr, val)
                logger.debug(f'Attribute "{attr}" SET “{val}”')
        except AttributeError as e:
            logger.info(e)


def register():
    bpy.utils.register_class(RenderNodeBase)


def unregister():
    bpy.utils.unregister_class(RenderNodeBase)
