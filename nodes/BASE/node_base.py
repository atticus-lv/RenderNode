import bpy

from bpy.props import *
from mathutils import Color, Vector

from ._runtime import cache_node_dependants, cache_socket_links, cache_socket_variables, cache_node_group_outputs, \
    runtime_info, logger
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
        if self.bl_idname == 'RSNodeTaskNode': self.label = self.name
        if hasattr(self, 'is_active_task'): self.is_active_task = False
        print(f"RSN Copied {self.name} from {node.name}")

    def free(self):
        """Remove Node"""
        print("RSN removed node", self.name)

    ## INITIAL METHOD
    #########################################

    node_dict = {}

    def create_input(self, socket_type, socket_name, socket_label, default_value=None):
        if self.inputs.get(socket_name):
            return None

        input = self.inputs.new(socket_type, socket_name)
        input.text = socket_label

        if default_value: input.default_value = default_value

    def remove_input(self, socket_name):
        input = self.inputs.get(socket_name)
        if input:
            self.inputs.remove(input)

    def create_output(self, socket_type, socket_name, socket_label, default_value=None):
        if self.outputs.get(socket_name):
            return None

        output = self.outputs.new(socket_type, socket_name)
        output.text = socket_label

        if default_value: output.default_value = default_value

    def remove_output(self, socket_name):
        output = self.outputs.get(socket_name)
        if output:
            self.outputs.remove(output)

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
        if self.last_ex_id == id:
            return

        self.last_ex_id = id

        self.execute_dependants(context, id, path)
        self.process_group(context, id, path)
        self.process(context, id, path)

        print(f'Execute: <{self.name}>')

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
        if runtime_info['updating'] is True:
            return

        # for input in self.inputs:
        #     input.remove_incorrect_links()

    def auto_update_inputs(self, socket_type='RSNodeSocketTaskSettings', socket_name='Input'):
        """add or remove inputs automatically
        :parm socket_type: any socket type that is registered in blender
        :parm socket_name: custom name for the socket
        """
        i = 0
        for input in self.inputs:
            if not input.is_linked:
                # keep at least one input for links with py commands
                if i == 0:
                    i += 1
                else:
                    self.inputs.remove(input)
        # auto add inputs
        if i != 1: self.inputs.new(socket_type, socket_name)

    ## RSN DATA MANAGE
    #########################################

    # update the build-in values with update the hole tree
    def execute_tree(self):
        self.id_data.execute(bpy.context)

    def get_input_value(self, socket_name):
        ans = self.inputs.get(socket_name)
        if ans: return ans.get_value()

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
