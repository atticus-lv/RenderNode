import bpy
import nodeitems_utils
from bpy.props import EnumProperty, IntProperty, StringProperty

from ...preferences import get_pref


class RSN_OT_SearchAndLink(bpy.types.Operator):
    bl_idname = "rsn.search_and_link"
    bl_label = "Search Add"
    bl_property = "my_search"
    bl_options = {"REGISTER", "UNDO"}

    nt = None
    node_name: StringProperty()
    input_id: IntProperty()
    output_id: IntProperty()

    my_search: EnumProperty(
        name="My Search",
        items=[('RSNodeTaskNode', 'Task', ''), ('RSNodeRenderListNode', 'Render List', ''),
               ('RSNodeProcessorNode', 'Processor', ''), ('RSNodeViewerNode', 'Viewer', ''),
               ('RSNodeVariantsNode', 'Variants', ''), ('RSNodeSetVariantsNode', 'Set Variants', ''),
               ('RSNodeNullNode', 'Null', ''), ('RSNodeCommonSettingsNode', 'Common Settings', ''),
               ('RSNodePropertyInputNode', 'Property', ''), ('RSNodeCamInputNode', 'Camera', ''),
               ('RSNodeWorldInputNode', 'World', ''), ('RSNodeViewLayerInputNode', 'View Layer', ''),
               ('RSNodeColorManagementNode', 'Color Management', ''),
               ('RSNodeTaskInfoInputsNode', 'Task Info(Experiment)', ''),
               ('RSNodeCollectionDisplayNode', 'Collection Display', ''),
               ('RenderNodeObjectDisplay', 'Object Display', ''), ('RSNodeObjectMaterialNode', 'Object Material', ''),
               ('RSNodeObjectPSRNode', 'Object PSR', ''), ('RSNodeObjectDataNode', 'Object Data', ''),
               ('RSNodeObjectModifierNode', 'Object Modifier', ''), ('RSNodeFilePathInputNode', 'File Path', ''),
               ('RSNodeResolutionInputNode', 'Resolution', ''), ('RSNodeFrameRangeInputNode', 'Frame Range', ''),
               ('RSNodeImageFormatInputNode', 'Image Format', ''), ('RSNodeActiveRenderSlotNode', 'Render Slot', ''),
               ('RSNodeViewLayerPassesNode', 'View Layer Passes', ''),
               ('RSNodeWorkBenchRenderSettingsNode', 'WorkBench Settings', ''),
               ('RSNodeEeveeRenderSettingsNode', 'Eevee Settings', ''),
               ('RSNodeCyclesRenderSettingsNode', 'Cycles Settings', ''),
               ('RSNodeCyclesLightPathNode', 'Cycles Light Path', ''),
               ('RSNodeOctaneRenderSettingsNode', 'Octane Settings', ''),
               ('RSNodeLuxcoreRenderSettingsNode', 'Luxcore Settings', ''), ('RSNodeScriptsNode', 'Scripts', ''),
               ('RSNodeSmtpEmailNode', 'SMTP Email', ''), ('RSNodeLightStudioNode', 'SSM Light Studio', ''),
               ('RSNodeSettingsMergeNode', 'Merge', ''), ('RSNodeSettingsMergeNode', 'Switch', '')])

    def node_enum_items(self, context):
        node_items_list = []
        for index, item in enumerate(nodeitems_utils.node_items_iter(context)):
            if isinstance(item, nodeitems_utils.NodeItem):
                node_items_list.append((item.nodetype, item.label, ''))

        print(node_items_list)
        return node_items_list

    def execute(self, context):

        #
        # print(self.node)
        # print(f"{self.nt}.{self.input_id}")
        # print(self.node.outputs[0])
        # try:
        #     pass
        #     # nt.links.new(new_node.outputs[0], eval(f"{nt}.{self.input_id}"))
        # except Exception as e:
        #     print(e)

        # print(self.input_id)
        # print(self.output_id)
        # print(self.my_search)

        # id = self.input_id[-2:-1]
        # node_name = input_id[]

        # self.node_enum_items(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.nt = context.space_data.node_tree
        print(self.input_id)
        print(self.output_id)
        print(self.node_name)
        context.window_manager.invoke_search_popup(self)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SearchAndLink)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SearchAndLink)
