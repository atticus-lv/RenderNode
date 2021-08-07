import bpy

from bpy.props import *
from mathutils import Color, Vector

from ._runtime import cache_node_dependants, cache_socket_links, runtime_info, logger


# some method comes from rigging_nodes
class RenderNodeBase(bpy.types.Node):
    bl_label = "RenderStack Node"

    warning: BoolProperty(name='Is warning', default=False)
    warning_msg: StringProperty(name='warning message', default='')

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'

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

    def execute_dependants(self):
        '''Responsible of executing the required nodes for the current node to work'''
        for x in self.get_dependant_nodes():
            self.execute_other(x)

    def execute(self):
        self.execute_dependants()
        self.process()
        print(f'Execute: <{self.name}>')

    def execute_other(self, other):
        if hasattr(other, 'execute'):
            other.execute()

    def update(self):
        if runtime_info['updating']:
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

    # update the build-in values
    def update_parms(self):
        task_node = self.id_data.nodes.get(bpy.context.window_manager.rsn_viewer_node)
        if task_node:
            task_node.execute()

    def get_input_value(self, socket_name):
        ans = self.inputs.get(socket_name)
        if ans: return ans.get_value()

    #  store socket
    def store_data(self):
        for input in self.inputs:
            if input.is_linked:
                node = self.reroute_socket_node(input, self)
                print(f'accept result:{node}')
                if hasattr(node, 'value'):
                    self.node_dict[input.name] = self.transfer_value(node.default_value)
                    self.node_dict[input.name] = self.transfer_value(node.default_value)
            else:
                self.node_dict[input.name] = self.transfer_value(input.default_value)

    def transfer_value(self, value):

        return list(value) if type(value) in {Color, Vector} else value

    def process(self):
        pass

    ### old method ###
    def get_data(self):
        """For get self date into rsn tree method"""
        pass

    ## Utility
    #########################################
    @staticmethod
    def reroute_socket_node(socket, node, target_node_type=None):
        def get_sub_node(socket, node):
            if socket.is_linked:
                sub_node = socket.links[0].from_node
                if len(sub_node.inputs) == 0: return sub_node
                return get_sub_node(sub_node.inputs[0], sub_node)

        return get_sub_node(socket, node)

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
