import json
import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RenderListNode_OT_GetInfo(bpy.types.Operator):
    bl_idname = "renderlistnode.get_info"
    bl_label = "Get Info"

    data:StringProperty()
    fill_text: BoolProperty(default=False)
    flatten_data: BoolProperty(default=False)

    def update(self, node):
        def process(node, input=None):
            if hasattr(node, "process"):
                node.process()
                print(f"Processing'{node.name}-{input.name if input else 'self'}'")

        def update_nodes(node):
            for input in node.inputs:
                if input.is_linked:
                    sub_node = input.links[0].from_node
                    update_nodes(sub_node)
                else:
                    process(node, input=input)
            process(node)

        update_nodes(node)
        print("< - update nodes finished - >")

    def get_data(self):
        node_tree = bpy.context.space_data.edit_tree
        active_node = node_tree.nodes.active
        self.update(active_node)
        input_node = active_node.inputs[0].links[0].from_node
        data = input_node.outputs[0][input_node.outputs[0].name].to_dict()
        return data

    def transfer_data(self):
        self.data = json.dumps(self.get_data())

    def execute(self, context):

        if self.fill_text:
            try:
                file = bpy.data.texts['Info Node']
                file.clear()
            except:
                file = bpy.data.texts.new('Info Node')

            json_data = json.dumps(self.get_data(), indent=4,
                                   ensure_ascii=False, sort_keys=False, separators=(',', ':'))
            file.write(json_data)

        return {"FINISHED"}

class RSNodeInfoNode(RenderStackNode):
    bl_idname = 'RSNodeRenderInfoNode'
    bl_label = 'Info'

    def init(self, context):
        self.inputs.new('NodeSocketString', "Info")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.operator("renderlistnode.get_info").fill_text = 1


def register():
    bpy.utils.register_class(RenderListNode_OT_GetInfo)
    bpy.utils.register_class(RSNodeInfoNode)

def unregister():
    bpy.utils.unregister_class(RenderListNode_OT_GetInfo)
    bpy.utils.unregister_class(RSNodeInfoNode)