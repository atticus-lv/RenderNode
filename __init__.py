bl_info = {
    "name"       : "RenderStack Node",
    "author"     : "Atticus",
    "version"    : (0, 1),
    "blender"    : (2, 90, 0),
    "location"   : "Node Editor",
    "description": "Node based render queue workflow",
    # "doc_url"    : "",
    "category"   : "Render",
}

import bpy
import nodeitems_utils
from bpy.props import *


class GetNodeInfo():
    def __init__(self, node_tree):
        self.nt = node_tree

    def get_renderlist_nodes(self):
        node_list = [node for node in self.nt.nodes if node.bl_idname == "RSNodeSocketRenderList"]
        return node_list

    def get_active_node(self):
        return self.nt.nodes.active

    @staticmethod
    def get_task_nodes(renderlist_node):
        task_list = {}
        for i, input in renderlist_node.inputs:
            if input.is_linked:
                task_list[i] = {"node": input.links[0].from_node}

        return task_list

    @staticmethod
    def get_camera_settings_node(task_node):
        if task_node.inputs[0].is_linked:
            return task_node.inputs[0].links[0].from_node

    @staticmethod
    def get_render_settings_node(task_node):
        if task_node.inputs[1].is_linked:
            return task_node.inputs[1].links[0].from_node

    @staticmethod
    def get_output_settings_node(task_node):
        if task_node.inputs[2].is_linked:
            return task_node.inputs[2].links[0].from_node


class RenderStackNodeTree(bpy.types.NodeTree):
    '''RenderStackNodeTree Node Tree'''
    bl_idname = 'RenderStackNodeTree'
    bl_label = 'RenderStack Node'
    bl_icon = 'BLENDER'


class RenderStackNode(bpy.types.Node):
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'

    def copy(self, node):
        print("copied node", node)

    def free(self):
        print("Node removed", self)

    def get_items_dict(self):
        return self.items()

    def get_active_node(self):
        node_tree = bpy.context.space_data.edit_tree
        return node_tree.nodes.active


class RSNodeSocketCamera(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketCamera'
    bl_label = 'RSNodeSocketCamera'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.2, 0.2, 1.0, 1.0)


class RSNodeSocketCameraSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketCameraSettings'
    bl_label = 'RSNodeSocketCameraSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.5, 0.5, 1.0, 1.0)


class RSNodeSocketRenderSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderSettings'
    bl_label = 'RSNodeSocketRenderSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (1, 0.2, 1.0, 1.0)


class RSNodeSocketOutputSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketOutputSettings'
    bl_label = 'RSNodeSocketOutputSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (1.0, 1.0, 1.0, 1.0)


class RSNodeSocketRenderList(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderList'
    bl_label = 'RSNodeSocketRenderList'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.5, 0.3, 0.7, 1.0)


class RSNodeIntValueNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeIntValueNode'
    bl_label = 'Int'

    value: IntProperty(name="Value", default=0)

    def init(self, context):
        self.outputs.new('NodeSocketInt', "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value')


def poll_camera(self, object):
    return object.type == 'CAMERA'


class RSNodeCamInputNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCamInputNode'
    bl_label = 'Camera'

    camera: PointerProperty(name="Camera", type=bpy.types.Object, poll=poll_camera)

    def init(self, context):
        self.outputs.new('RSNodeSocketCamera', "Camera")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'camera', text="")

    def process(self, context):
        pass


class RSNodeCameraSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCameraSettingsNode'
    bl_label = 'Camera Settings'

    def init(self, context):
        self.inputs.new('RSNodeSocketCamera', "Camera")
        self.inputs.new('NodeSocketInt', "Res X")
        self.inputs.new('NodeSocketInt', "Res Y")
        self.inputs.new('NodeSocketInt', "Res Scale")

        self.outputs.new('RSNodeSocketCameraSettings', "Cam Settings")

        self.inputs["Res X"].default_value = 1920
        self.inputs["Res Y"].default_value = 1080
        self.inputs["Res Scale"].default_value = 100

    def draw_buttons(self, context, layout):
        pass


class RSNodeCyclesRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCyclesRenderSettingsNode'
    bl_label = 'Cycles Settings'

    samples: IntProperty(default=128, name='Samples', min=4)

    def init(self, context):
        self.inputs.new('NodeSocketInt', "Samples")
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

        self.inputs["Samples"].default_value = 128

    def draw_buttons(self, context, layout):
        pass


class RSNodeOutputSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeOutputSettingsNode'
    bl_label = 'Output Settings'

    def init(self, context):
        self.inputs.new('NodeSocketInt', 'Frame Start')
        self.inputs.new('NodeSocketInt', 'Frame End')
        self.inputs.new('NodeSocketInt', 'Frame Step')
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

        self.inputs["Frame Step"].default_value = 1

    def draw_buttons(self, context, layout):
        pass


class RSNodeTaskNode(RenderStackNode):
    '''A simple Task node'''
    bl_idname = 'RSNodeTaskNode'
    bl_label = 'Task'

    def init(self, context):
        self.inputs.new('RSNodeSocketCameraSettings', "Camera Settings")
        self.inputs.new('RSNodeSocketRenderSettings', "Render Settings", )
        self.inputs.new('RSNodeSocketOutputSettings', "Output Settings")

        self.outputs.new('RSNodeSocketRenderList', "Render List")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'name')


class RenderListNode_OT_GetInfo(bpy.types.Operator):
    bl_idname = "renderlistnode.get_info"
    bl_label = "Get Info"

    def execute(self, context):
        info = GetNodeInfo(bpy.context.space_data.edit_tree)
        list_node = info.get_active_node()
        task_nodes = list_node.get_task_nodes(list_node)

        return {"FINISHED"}


class RenderListNode_OT_EditInput(bpy.types.Operator):
    bl_idname = "renderlistnode.edit_input"
    bl_label = "Add Task"

    remove: BoolProperty(name="remove action", default=False)

    def execute(self, context):
        node_tree = bpy.context.space_data.edit_tree
        active_node = node_tree.nodes.active
        if not self.remove:
            active_node.inputs.new('RSNodeSocketRenderList', f"Task {len(active_node.inputs) + 1}")

        return {"FINISHED"}


class RSNodeRenderListNode(RenderStackNode):
    '''Render List Node'''
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    name: StringProperty(name="Name", default="Task")

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task 1")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.operator("renderlistnode.edit_input")


class RenderStackNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderStackNodeTree'


node_categories = [

    RenderStackNodeCategory("VALUES", "Values", items=[
        nodeitems_utils.NodeItem("RSNodeIntValueNode"),
    ]),

    RenderStackNodeCategory("CAMERASETTINGS", "Camera Settings", items=[
        nodeitems_utils.NodeItem("RSNodeCamInputNode"),
        nodeitems_utils.NodeItem("RSNodeCameraSettingsNode"),
    ]),

    RenderStackNodeCategory("RENDERSETTINGS", "Render Settings", items=[
        nodeitems_utils.NodeItem("RSNodeCyclesRenderSettingsNode"),

    ]),

    RenderStackNodeCategory("OUTPUTSETTINGS", "Output Settings", items=[
        nodeitems_utils.NodeItem("RSNodeOutputSettingsNode"),
    ]),

    RenderStackNodeCategory("ROP", "Render Output", items=[
        nodeitems_utils.NodeItem("RSNodeTaskNode"),
        nodeitems_utils.NodeItem("RSNodeRenderListNode"),

    ]),

]

classes = [
    # node tree
    RenderStackNodeTree,
    # node socket
    RSNodeSocketCamera,
    RSNodeSocketCameraSettings,
    RSNodeSocketRenderSettings,
    RSNodeSocketOutputSettings,
    RSNodeSocketRenderList,
    # nodes
    RSNodeIntValueNode,
    RSNodeCyclesRenderSettingsNode,
    RSNodeOutputSettingsNode,

    RSNodeCamInputNode,
    RSNodeCameraSettingsNode,
    RSNodeTaskNode,
    RSNodeRenderListNode,
    RenderListNode_OT_EditInput, RenderListNode_OT_GetInfo
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    nodeitems_utils.register_node_categories("RENDERSTACK_NODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("RENDERSTACK_NODES")

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    try:
        nodeitems_utils.unregister_node_categories("CUSTOM_NODES")
    except:
        pass
    finally:
        register()
