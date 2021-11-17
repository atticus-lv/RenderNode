from bpy.props import *
from ...utility import *
from ...nodes.BASE.node_base import RenderNodeBase
from ...ui.icon_utils import RSN_Preview

from ..BASE._runtime import cache_node_dependants


def update_active_task(self, context):
    if self.is_active_list:
        for node in self.id_data.nodes:
            if node.bl_idname == 'RenderNodeTaskRenderListNode' and node != self:
                node.is_active_list = False
    bpy.context.window_manager.rsn_active_list = self.name
    bpy.context.scene.rsn_bind_tree = self.id_data  # bind tree
    self.execute_tree()


class RenderNodeTaskRenderListNode(RenderNodeBase):
    """Render List Node"""
    bl_idname = 'RenderNodeTaskRenderListNode'
    bl_label = 'Task Render List'

    active_index: IntProperty(name="Set Active Task", min=0, update=update_active_task)
    is_active_list: BoolProperty(name="Active List")

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'RenderStackNodeTree'}

    def draw_buttons(self, context, layout):
        layout.box().prop(self, 'is_active_list')
        layout.prop(self, 'active_index')

    def update(self):
        self.auto_update_inputs('RenderNodeSocketTask', "Task")

    def get_dependant_nodes(self):
        '''returns the nodes connected to the inputs of this node'''
        dep_tree = cache_node_dependants.setdefault(self.id_data, {})
        nodes = []

        for index, input in enumerate(self.inputs):
            if index == self.active_index:
                connected_socket = input.connected_socket
                if connected_socket and connected_socket not in nodes:
                    nodes.append(connected_socket.node)
                break

            dep_tree[self] = nodes
        return nodes

    def process(self, context, id, path):
        pass


def register():
    bpy.utils.register_class(RenderNodeTaskRenderListNode)


def unregister():
    bpy.utils.unregister_class(RenderNodeTaskRenderListNode)
