import bpy
import nodeitems_utils


class RSNCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderStackNodeTree'


node_categories = [
    RSNCategory("TASK", "Task", items=[
        nodeitems_utils.NodeItem("RenderNodeTask"),
        nodeitems_utils.NodeItem("RSNodeRenderListNode"),
    ]),

    RSNCategory("INPUT", "Input", items=[
        nodeitems_utils.NodeItem('RenderNodeFloatInput'),
        nodeitems_utils.NodeItem('RenderNodeVectorInput'),
        nodeitems_utils.NodeItem('RenderNodeBoolInput'),
        nodeitems_utils.NodeItem('RenderNodeIntInput'),
        nodeitems_utils.NodeItem('RenderNodeStringInput'),
        nodeitems_utils.NodeItem('RenderNodeObjectInput'),
        nodeitems_utils.NodeItem('RenderNodeMaterialInput'),
        nodeitems_utils.NodeItem('RenderNodeInfoInput'),
    ]),

    RSNCategory("UTILITY", "Utility", items=[
        nodeitems_utils.NodeItem("RenderNodeMath"),
        nodeitems_utils.NodeItem("RenderNodeVectorMath"),
        nodeitems_utils.NodeItem("RenderNodeBooleanMath"),
        nodeitems_utils.NodeItem("RenderNodeStringOperate"),
        nodeitems_utils.NodeItem("RenderNodeVectorConvert"),
        nodeitems_utils.NodeItem("RenderNodeProperty"),
        nodeitems_utils.NodeItem('RSNodeCollectionDisplayNode'),
        nodeitems_utils.NodeItem('RenderNodeScripts'),
    ]),

    RSNCategory("SCENE", "Scene", items=[
        nodeitems_utils.NodeItem("RenderNodeScene"),
        nodeitems_utils.NodeItem("RenderNodeSceneCamera"),
        nodeitems_utils.NodeItem("RenderNodeSceneWorld"),
    ]),

    RSNCategory("VIEWLAYER", "Scene ViewLayer", items=[
        nodeitems_utils.NodeItem("RenderNodeSceneViewLayer"),
    ]),

    RSNCategory("RENDER", "Scene Render", items=[
        nodeitems_utils.NodeItem("RenderNodeSceneRenderEngine"),
        nodeitems_utils.NodeItem("RenderNodeSceneColorManagement"),
        nodeitems_utils.NodeItem("RenderNodeCyclesLightPath"),
    ]),

    RSNCategory("OUTPUT", "Scene Output", items=[
        nodeitems_utils.NodeItem("RenderNodeSceneFilePath"),
        nodeitems_utils.NodeItem("RenderNodeSceneFrameRange"),
        nodeitems_utils.NodeItem("RenderNodeSceneImageFormat"),
        nodeitems_utils.NodeItem("RenderNodeSceneMovieFormat"),
        nodeitems_utils.NodeItem("RenderNodeSceneResolution"),  # performance is bad
        nodeitems_utils.NodeItem("RenderNodeSceneRenderSlot"),
    ]),

    RSNCategory("OBJECT", "Object", items=[
        nodeitems_utils.NodeItem('RenderNodeObjectDisplay'),
        nodeitems_utils.NodeItem('RenderNodeObjectMaterial'),
        nodeitems_utils.NodeItem('RenderNodeObjectPSR'),
        nodeitems_utils.NodeItem('RenderNodeObjectData'),
    ]),

    RSNCategory("VARIANTS", "Variants", items=[
        nodeitems_utils.NodeItem("RenderNodeSwitch"),
        nodeitems_utils.NodeItem("RenderNodeVariants"),
    ]),

    RSNCategory("COMP", "Compose", items=[
        nodeitems_utils.NodeItem("RenderNodeImageSequence"),
    ]),

    # RSNCategory("GROUP", "Group", items=[
    #     nodeitems_utils.NodeItem("RenderNodeGroup"),
    # ]),

    RSNCategory("LAYOUT", "Layout", items=[
        nodeitems_utils.NodeItem('RenderNodeMerge'),
        nodeitems_utils.NodeItem('NodeFrame'),
        nodeitems_utils.NodeItem('NodeReroute'),
    ]),

    RSNCategory("EXP", "Exp", items=[
        nodeitems_utils.NodeItem("RenderNodeEmailNode"),

    ]),

    RSNCategory("OLD", "Old(Not fully support now)", items=[
        nodeitems_utils.NodeItem("RSNodeCommonSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeScriptsNode"),
        nodeitems_utils.NodeItem("RSNodeSmtpEmailNode"),
        nodeitems_utils.NodeItem("RSNodeLightStudioNode"),
        nodeitems_utils.NodeItem("RSNodeWorkBenchRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeEeveeRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeCyclesRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeCyclesLightPathNode"),
        nodeitems_utils.NodeItem("RSNodeOctaneRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeLuxcoreRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeResolutionInputNode"),
        nodeitems_utils.NodeItem("RSNodeActiveRenderSlotNode"),
        nodeitems_utils.NodeItem("RSNodeViewLayerPassesNode"),
    ]),

    RSNCategory("SET", "Set", items=[
        nodeitems_utils.NodeItem("RenderNodeSetSceneCamera"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectMaterial"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneResolution"),
        nodeitems_utils.NodeItem("RenderNodeSetFilePath"),
        nodeitems_utils.NodeItem("RenderNodeGetListIndex"),
        nodeitems_utils.NodeItem("RenderNodeTaskInput"),
        nodeitems_utils.NodeItem("RenderNodeTaskRenderListNode"),

    ]),
]


def register():
    try:
        nodeitems_utils.unregister_node_categories("RSNCategory")
    except Exception:
        pass
    nodeitems_utils.register_node_categories("RSNCategory", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("RSNCategory")
