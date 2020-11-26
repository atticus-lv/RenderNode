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

import json

import bpy
import nodeitems_utils
from bpy.props import *


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
        print("Copied node", node)

    def free(self):
        print("Node removed", self)


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

    def process(self):
        dict = {}
        if self.camera:
            dict["name"] = self.camera.name
        else:
            dict["name"] = None
        self.outputs["Camera"]["Camera"] = dict


class RSNodeCameraSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCameraSettingsNode'
    bl_label = 'Camera Settings'

    def init(self, context):
        self.inputs.new('RSNodeSocketCamera', "Camera")
        self.inputs.new('NodeSocketInt', "Res X", )
        self.inputs.new('NodeSocketInt', "Res Y")
        self.inputs.new('NodeSocketInt', "Res Scale")

        self.outputs.new('RSNodeSocketCameraSettings', "Camera Settings")

        self.inputs["Res X"].default_value = 1920
        self.inputs["Res Y"].default_value = 1080
        self.inputs["Res Scale"].default_value = 100

    def draw_buttons(self, context, layout):
        pass

    def process(self):
        dict = {}
        for input in self.inputs:
            try:
                if input.is_linked:
                    dict[input.name] = input.links[0].from_socket[input.name]
                else:
                    try:
                        dict[input.name] = input.default_value
                    except:
                        pass
            except Exception as e:
                print(f"Camera Settings {e}")
        self.outputs["Camera Settings"]["Camera Settings"] = dict


class RSNodeEeveeRenderSettingsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeEeveeRenderSettingsNode'
    bl_label = 'Eevee Settings'

    samples: IntProperty(default=128, name='Samples', min=4)

    def init(self, context):
        self.inputs.new('NodeSocketInt', "Samples")
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

        self.inputs["Samples"].default_value = 128

    def draw_buttons(self, context, layout):
        pass

    def process(self):
        dict = {}
        dict["Engine"] = 'BLENDER_EEVEE'
        for input in self.inputs:
            try:
                if input.is_linked:
                    dict[input.name] = input.links[0].from_socket[input.name]
                else:
                    try:
                        dict[input.name] = input.default_value
                    except:
                        pass
            except Exception as e:
                print(f"Render Settings {e}")
        self.outputs["Render Settings"]["Render Settings"] = dict


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

    def process(self):
        dict = {}
        dict["Engine"] = "CYCLES"
        for input in self.inputs:
            try:
                if input.is_linked:
                    dict[input.name] = input.links[0].from_socket[input.name]
                else:
                    try:
                        dict[input.name] = input.default_value
                    except:
                        pass
            except Exception as e:
                print(f"Render Settings {e}")
        self.outputs["Render Settings"]["Render Settings"] = dict


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

    def process(self):
        dict = {}
        for input in self.inputs:
            try:
                if input.is_linked:
                    dict[input.name] = input.links[0].from_socket[input.name]
                else:
                    try:
                        dict[input.name] = input.default_value
                    except:
                        pass
            except Exception as e:
                print(f"Output Settings {e}")
        self.outputs["Output Settings"]["Output Settings"] = dict


class RSNodeTaskNode(RenderStackNode):
    '''A simple Task node'''
    bl_idname = 'RSNodeTaskNode'
    bl_label = 'Task'

    def init(self, context):
        self.inputs.new('RSNodeSocketCameraSettings', "Camera Settings")
        self.inputs.new('RSNodeSocketRenderSettings', "Render Settings", )
        self.inputs.new('RSNodeSocketOutputSettings', "Output Settings")

        self.outputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'name')

    def process(self):
        dict = {}
        dict["name"] = self.name

        for input in self.inputs:
            try:
                if input.is_linked:
                    dict[input.name] = input.links[0].from_socket[input.name]
                else:
                    try:
                        dict[input.name] = input.default_value
                    except:
                        pass
            except Exception as e:
                print(f"Task {e}")

        self.outputs["Task"]["Task"] = dict


class RenderListNode_OT_GetInfo(bpy.types.Operator):
    bl_idname = "renderlistnode.get_info"
    bl_label = "Get Info"

    value: StringProperty()

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

    def execute(self, context):
        node_tree = bpy.context.space_data.edit_tree
        active_node = node_tree.nodes.active
        self.update(active_node)
        input_node = active_node.inputs[0].links[0].from_node
        data = input_node.outputs[0][input_node.outputs[0].name].to_dict()
        json_data = json.dumps(data, indent=4,
                               ensure_ascii=False, sort_keys=False, separators=(',', ':'))
        self.value = json_data
        try:
            file = bpy.data.texts['Info Node']
            file.clear()
        except:
            file = bpy.data.texts.new('Info Node')
        file.write(json_data)

        return {"FINISHED"}


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
        layout.operator("renderlistnode.edit_input",text="Remove Unused").remove = True

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


class RSNodeSocketInfoNode(RenderStackNode):
    bl_idname = 'RSNodeRenderInfoNode'
    bl_label = 'Info'

    def init(self, context):
        self.inputs.new('NodeSocketString', "Task")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        layout.operator("renderlistnode.edit_input")


class RenderStackNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderStackNodeTree'


node_categories = [

    RenderStackNodeCategory("CAMERASETTINGS", "Camera Settings", items=[
        nodeitems_utils.NodeItem("RSNodeCamInputNode"),
        nodeitems_utils.NodeItem("RSNodeCameraSettingsNode"),
    ]),

    RenderStackNodeCategory("RENDERSETTINGS", "Render Settings", items=[
        nodeitems_utils.NodeItem("RSNodeCyclesRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeEeveeRenderSettingsNode"),

    ]),

    RenderStackNodeCategory("OUTPUTSETTINGS", "Output Settings", items=[
        nodeitems_utils.NodeItem("RSNodeOutputSettingsNode"),
    ]),

    RenderStackNodeCategory("ROP", "Render Output", items=[
        nodeitems_utils.NodeItem("RSNodeTaskNode"),
        nodeitems_utils.NodeItem("RSNodeRenderListNode"),

    ]),
    RenderStackNodeCategory("VIEWER", "Viewer", items=[
        nodeitems_utils.NodeItem("RSNodeRenderInfoNode"),

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
    RSNodeRenderInfoNode,
    RSNodeOutputSettingsNode,
    RSNodeCyclesRenderSettingsNode,
    RSNodeEeveeRenderSettingsNode,

    RSNodeCamInputNode,
    RSNodeCameraSettingsNode,

    RSNodeTaskNode,
    RSNodeRenderListNode,
    # operator
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
