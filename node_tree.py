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
        nodeitems_utils.NodeItem("RSNodeRenderViewerNode"),

    ]),

]

classes = [
    RenderStackNodeTree,
    RenderStackNode,
    RSNodeSocketCamera,
    RSNodeSocketCameraSettings,
    RSNodeSocketRenderSettings,
    RSNodeSocketOutputSettings,
    RSNodeSocketRenderList
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    nodeitems_utils.register_node_categories("RENDERSTACK_NODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("RENDERSTACK_NODES")

    for cls in classes:
        bpy.utils.unregister_class(cls)
