import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RenderListNode_OT_EditInput(bpy.types.Operator):
    bl_idname = "renderlistnode.edit_input"
    bl_label = "Add Task"

    remove: BoolProperty(name="remove action", default=False)

    def execute(self, context):
        node_tree = bpy.context.space_data.edit_tree
        active_node = node_tree.nodes.active
        if not self.remove:
            active_node.inputs.new('RSNodeSocketRenderList', "Task")
        else:
            for input in active_node.inputs:
                if not input.is_linked:
                    active_node.inputs.remove(input)

        return {"FINISHED"}

class RSNodeRenderListNode(RenderStackNode):
    '''Render List Node'''
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.outputs.new('NodeSocketInt', "Info")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.operator("renderlistnode.edit_input").remove = False
        layout.operator("renderlistnode.edit_input", text="Remove Unused").remove = True

    def process(self):
        dict = {}
        for i, input in enumerate(self.inputs):
            try:
                if input.is_linked:
                    dict[f"{i}"] = input.links[0].from_socket[input.name]
                else:
                    try:
                        dict[f"{i}"] = input.default_value
                    except:
                        pass
            except Exception as e:
                print(f"Info {e}")
        self.outputs["Info"]["Info"] = dict

def register():
    bpy.utils.register_class(RenderListNode_OT_EditInput)
    bpy.utils.register_class(RSNodeRenderListNode)

def unregister():
    bpy.utils.unregister_class(RenderListNode_OT_EditInput)
    bpy.utils.unregister_class(RSNodeRenderListNode)