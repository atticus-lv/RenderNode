import bpy
import nodeitems_utils
from bpy.props import *


class RenderStackNodeTree(bpy.types.NodeTree):
    '''RenderStackNodeTree Node Tree'''
    bl_idname = 'RenderStackNodeTree'
    bl_label = 'RenderStack Node'
    bl_icon = 'BLENDER'


class RenderStackNode(bpy.types.Node):
    bl_label = "RenderStack Node"

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)


class RenderStackNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderStackNodeTree'


#
#  Sockets
#


class RSNodeSocketCamera(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketCamera'
    bl_label = 'RSNodeSocketCamera'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0, 0.8, 1.0, 1.0)


class RSNodeSocketTaskSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketTaskSettings'
    bl_label = 'RSNodeSocketTaskSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 1.0)


class RSNodeSocketRenderSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderSettings'
    bl_label = 'RSNodeSocketRenderSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0, 1, 0, 1.0)


class RSNodeSocketOutputSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketOutputSettings'
    bl_label = 'RSNod   eSocketOutputSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0, 0, 1, 1.0)


class RSNodeSocketRenderList(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderList'
    bl_label = 'RSNodeSocketRenderList'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.5, 0.3, 0.7, 1.0)


node_categories = [

    RenderStackNodeCategory("CAMERA", "Camera", items=[
        nodeitems_utils.NodeItem("RSNodeCamInputNode"),
    ]),

    RenderStackNodeCategory("RENDER_ENGINES", "Render Engines", items=[
        nodeitems_utils.NodeItem("RSNodeSettingsMergeNode", label="Merge Render Settings", settings={
            "node_type": repr("RENDER_SETTINGS"),
        }),
        nodeitems_utils.NodeItem("RSNodeWorkBenchRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeEeveeRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeCyclesRenderSettingsNode"),

    ]),

    RenderStackNodeCategory("OUTPUT_SETTINGS", "Output Settings", items=[
        nodeitems_utils.NodeItem("RSNodeSettingsMergeNode", label="Merge Output Settings", settings={
            "node_type": repr("OUTPUT_SETTINGS"),
        }),

        nodeitems_utils.NodeItem("ResolutionInputNode"),
        nodeitems_utils.NodeItem("FrameRangeInputNode"),
        nodeitems_utils.NodeItem("ImageFormatInputNode"),
        nodeitems_utils.NodeItem("FilePathInputNode"),
    ]),

    RenderStackNodeCategory("TASK", "Task", items=[
        nodeitems_utils.NodeItem("RSNodeTaskNode"),
        nodeitems_utils.NodeItem("RSNodeRenderListNode"),

    ]),

    RenderStackNodeCategory("SCRIPTS", "Scripts", items=[
        nodeitems_utils.NodeItem("RSSettingsScriptsNode"),
        nodeitems_utils.NodeItem("RSFileScriptsNode"),

    ]),


]

classes = [
    RenderStackNodeTree,
    RenderStackNode,
    RSNodeSocketCamera,
    RSNodeSocketRenderSettings,
    RSNodeSocketOutputSettings,
    RSNodeSocketTaskSettings,
    RSNodeSocketRenderList,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    nodeitems_utils.register_node_categories("RENDERSTACK_NODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("RENDERSTACK_NODES")

    for cls in classes:
        bpy.utils.unregister_class(cls)
