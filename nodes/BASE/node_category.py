import bpy
import nodeitems_utils


class RSNCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderNodeTree'


node_categories = [
    RSNCategory("INPUT", "Input", items=[
        nodeitems_utils.NodeItem("RenderNodeTaskInput"),
        nodeitems_utils.NodeItem("RenderNodeRandomInput"),
        nodeitems_utils.NodeItem('RenderNodeFloatInput'),
        nodeitems_utils.NodeItem('RenderNodeBoolInput'),
        nodeitems_utils.NodeItem('RenderNodeIntInput'),
        nodeitems_utils.NodeItem('RenderNodeVectorInput'),
        nodeitems_utils.NodeItem('RenderNodeStringInput'),
        nodeitems_utils.NodeItem('RenderNodeObjectInput'),
        nodeitems_utils.NodeItem('RenderNodeGetCameraInfo'),
        nodeitems_utils.NodeItem('RenderNodeMaterialInput'),
        nodeitems_utils.NodeItem('RenderNodeActionInput'),
    ]),

    RSNCategory("LIST", "List", items=[
        nodeitems_utils.NodeItem("RenderNodeGetListIndex"),
        nodeitems_utils.NodeItem("RenderNodeTaskRenderListNode"),
    ]),

    RSNCategory("UTILITY", "Utility", items=[
        nodeitems_utils.NodeItem("RenderNodeSwitch"),
        nodeitems_utils.NodeItem("RenderNodeMath"),
        nodeitems_utils.NodeItem("RenderNodeVectorMath"),
        nodeitems_utils.NodeItem("RenderNodeBooleanMath"),
        nodeitems_utils.NodeItem("RenderNodeStringOperate"),
        # nodeitems_utils.NodeItem("RenderNodeProperty"),
        nodeitems_utils.NodeItem('RenderNodeScripts'),
    ]),
    RSNCategory("CONVERT", "Convert", items=[
        nodeitems_utils.NodeItem("RenderNodeInt2Str"),
        nodeitems_utils.NodeItem("RenderNodeStr2Int"),
        nodeitems_utils.NodeItem("RenderNodeText2Str"),
        nodeitems_utils.NodeItem("RenderNodeVector2Float"),
        nodeitems_utils.NodeItem("RenderNodeFloat2Vector"),

    ]),

    RSNCategory("SCENE", "Scene", items=[
        nodeitems_utils.NodeItem("RenderNodeGetSceneCamera"),
        nodeitems_utils.NodeItem("RenderNodeGetSceneWorld"),
        nodeitems_utils.NodeItem("RenderNodeGetSceneRenderEngine"),
        nodeitems_utils.NodeItem("RenderNodeGetSceneViewLayer"),

        nodeitems_utils.NodeItem("RenderNodeSetSceneCamera"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneWorld"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneRenderEngine"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneSimplify"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneColorManagement"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneViewLayer"),
    ]),

    RSNCategory("EEVEE_CYCLES", "Eevee / Cycles", items=[
        nodeitems_utils.NodeItem("RenderNodeSetWorkBenchSamples"),
        nodeitems_utils.NodeItem("RenderNodeSetWorkBenchColor"),
        nodeitems_utils.NodeItem("RenderNodeSetWorkBenchOptions"),

        nodeitems_utils.NodeItem("RenderNodeSetEeveeSamples"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesSamplesViewport"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesSamplesRender"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesPerformance"),
        nodeitems_utils.NodeItem("RenderNodeSetEeveeAmbientOcclusion"),
        nodeitems_utils.NodeItem("RenderNodeSetEeveeBloom"),
        nodeitems_utils.NodeItem("RenderNodeSetEeveeDepthOfField"),
        nodeitems_utils.NodeItem("RenderNodeSetEeveeScreenSpaceReflections"),
        nodeitems_utils.NodeItem("RenderNodeSetEeveeMotionBlur"),

        nodeitems_utils.NodeItem("RenderNodeSetCyclesSamples"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesLightPathsMaxBounces"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesLightPathsClamping"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesLightPathsCaustics"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesLightPathsFastGI"),
    ]),

    RSNCategory("OUTPUT", "Output", items=[
        nodeitems_utils.NodeItem("RenderNodeGetSceneResolution"),

        nodeitems_utils.NodeItem("RenderNodeSetFilm"),
        nodeitems_utils.NodeItem("RenderNodeSetRenderSlot"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneResolution"),
        nodeitems_utils.NodeItem("RenderNodeSetFilePath"),
        nodeitems_utils.NodeItem("RenderNodeSetFrameRange"),
        nodeitems_utils.NodeItem("RenderNodeSetFileFormatImage"),
        nodeitems_utils.NodeItem("RenderNodeSetFileFormatMovie"),
    ]),

    RSNCategory("OBJECT", "Object", items=[
        nodeitems_utils.NodeItem("RenderNodeGetMaterial"),
        nodeitems_utils.NodeItem("RenderNodeGetObjectInfo"),
        nodeitems_utils.NodeItem("RenderNodeGetObjectVisibility"),
        nodeitems_utils.NodeItem("RenderNodeGetAction"),
        nodeitems_utils.NodeItem("RenderNodeGetActionFrameRange"),

        nodeitems_utils.NodeItem("RenderNodeSetObjectLocation"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectRotation"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectScale"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectMaterial"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectVisibility"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectAction"),
    ]),

    RSNCategory("COLLECTION", "Collection", items=[
        nodeitems_utils.NodeItem("RenderNodeGetCollectionVisibility"),
        nodeitems_utils.NodeItem("RenderNodeSetCollectionVisibility"),
    ]),

    RSNCategory("LAYOUT", "Layout", items=[
        # nodeitems_utils.NodeItem('RenderNodeMerge'),
        nodeitems_utils.NodeItem('NodeFrame'),
        nodeitems_utils.NodeItem('NodeReroute'),
    ]),

    RSNCategory("EXTRA", "Extra", items=[
        nodeitems_utils.NodeItem('RenderNodeEmailNode'),
        nodeitems_utils.NodeItem('RenderNodeGetTaskInfo'),
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
