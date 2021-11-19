import bpy
import nodeitems_utils


class RSNCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderStackNodeTree'


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
        nodeitems_utils.NodeItem("RenderNodeVectorConvert"),
        # nodeitems_utils.NodeItem("RenderNodeProperty"),
        nodeitems_utils.NodeItem('RenderNodeScripts'),
    ]),

    RSNCategory("SCENE", "Scene", items=[
        nodeitems_utils.NodeItem("RenderNodeSetSceneCamera"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneWorld"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneRenderEngine"),
    ]),

    RSNCategory("EEVEE_CYCLES", "Eevee / Cycles", items=[
        nodeitems_utils.NodeItem("RenderNodeSetEeveeSamples"),
        nodeitems_utils.NodeItem("RenderNodeSetEeveeAmbientOcclusion"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesLightPath"),
        nodeitems_utils.NodeItem("RenderNodeSetCyclesSamples"),
    ]),

    RSNCategory("OUTPUT", "Output", items=[
        nodeitems_utils.NodeItem("RenderNodeSetRenderSlot"),
        nodeitems_utils.NodeItem("RenderNodeSetSceneResolution"),
        nodeitems_utils.NodeItem("RenderNodeSetFilePath"),
        nodeitems_utils.NodeItem("RenderNodeSetFrameRange"),
        nodeitems_utils.NodeItem("RenderNodeSetFileFormatImage"),
        nodeitems_utils.NodeItem("RenderNodeSetFileFormatMovie"),
    ]),

    RSNCategory("OBJECT", "Object", items=[
        nodeitems_utils.NodeItem("RenderNodeGetMaterial"),
        nodeitems_utils.NodeItem("RenderNodeGetObjectVisibility"),
        nodeitems_utils.NodeItem("RenderNodeGetAction"),
        nodeitems_utils.NodeItem("RenderNodeGetActionFrameRange"),

        nodeitems_utils.NodeItem("RenderNodeSetObjectMaterial"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectVisibility"),
        nodeitems_utils.NodeItem("RenderNodeSetObjectAction"),
    ]),

    RSNCategory("COLLECTION", "Collection", items=[
        nodeitems_utils.NodeItem("RenderNodeSetCollectionVisibility"),
    ]),

    RSNCategory("LAYOUT", "Layout", items=[
        # nodeitems_utils.NodeItem('RenderNodeMerge'),
        nodeitems_utils.NodeItem('NodeFrame'),
        nodeitems_utils.NodeItem('NodeReroute'),
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
