import bpy
import nodeitems_utils


class RSNCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderStackNodeTree'


node_categorys = [
    RSNCategory("TASK", "Task", items=[
        nodeitems_utils.NodeItem("RSNodeTaskNode"),
        # nodeitems_utils.NodeItem("RSNodeTaskListNode"),
        nodeitems_utils.NodeItem("RSNodeRenderListNode"),
        nodeitems_utils.NodeItem("RSNodeProcessorNode"),
        nodeitems_utils.NodeItem("RSNodeViewerNode"),

    ]),
    RSNCategory("INPUT", "Input", items=[
        nodeitems_utils.NodeItem("RSNodeCamInputNode"),
        nodeitems_utils.NodeItem("RSNodeWorldInputNode"),
        nodeitems_utils.NodeItem('RSNodeViewLayerInputNode'),
        nodeitems_utils.NodeItem('RSNodeColorManagementNode'),
        nodeitems_utils.NodeItem("RSNodeTaskInfoInputsNode"),
    ]),

    RSNCategory("OBJECT", "Object", items=[
        nodeitems_utils.NodeItem('RSNodeObjectDisplayNode'),
        nodeitems_utils.NodeItem('RSNodeObjectMaterialNode'),
        nodeitems_utils.NodeItem('RSNodeObjectPSRNode'),
        # nodeitems_utils.NodeItem('RSNodeObjectDataNode'),
    ]),

    RSNCategory("OUTPUT_SETTINGS", "Output Settings", items=[
        nodeitems_utils.NodeItem("RSNodeResolutionInputNode"),
        nodeitems_utils.NodeItem("RSNodeFrameRangeInputNode"),
        nodeitems_utils.NodeItem("RSNodeImageFormatInputNode"),
        nodeitems_utils.NodeItem("RSNodeFilePathInputNode"),
        nodeitems_utils.NodeItem("RSNodeActiveRenderSlotNode"),
        nodeitems_utils.NodeItem("RSNodeViewLayerPassesNode"),
    ]),

    RSNCategory("RENDER_SETTINGS", "Render Settings", items=[
        nodeitems_utils.NodeItem("RSNodeWorkBenchRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeEeveeRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeCyclesRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeCyclesLightPathNode"),
        nodeitems_utils.NodeItem("RSNodeLuxcoreRenderSettingsNode"),
    ]),

    RSNCategory("SCRIPTS", "Scripts", items=[
        nodeitems_utils.NodeItem("RSNodeScriptsNode"),
        nodeitems_utils.NodeItem("RSNodeSmtpEmailNode"),
        nodeitems_utils.NodeItem("RSNodeLightStudioNode"),
        # nodeitems_utils.NodeItem("RSNodeServerNode"),
        # nodeitems_utils.NodeItem("RSNodeClientNode"),
    ]),
    RSNCategory("LAYOUT", "Layout", items=[
        nodeitems_utils.NodeItem("RSNodeSettingsMergeNode", label="Merge Settings", settings={
            "node_type": repr("MERGE"),
        }),
        nodeitems_utils.NodeItem("RSNodeSettingsMergeNode", label="Switch Settings", settings={
            "node_type": repr("SWITCH"),
            "label"    : repr("Switch Settings"),
        }),
    ]),
]


def register():
    try:
        nodeitems_utils.unregister_node_categories("RSNCategory")
    except:
        pass
    nodeitems_utils.register_node_categories("RSNCategory", node_categorys)


def unregister():
    nodeitems_utils.unregister_node_categories("RSNCategory")
