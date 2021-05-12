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
        new_node = context.space_data.edit_tree.nodes.new(type=self.my_search)

        try:
            if self.input_id != 666:
                context.space_data.edit_tree.links.new(
                    context.space_data.edit_tree.nodes[self.node_name].inputs[self.input_id],
                    new_node.outputs[0])

            elif self.output_id != 666:
                context.space_data.edit_tree.links.new(
                    context.space_data.edit_tree.nodes[self.node_name].outputs[self.output_id],
                    new_node.inputs[0])

        except Exception as e:
            print(e)

        context.space_data.edit_tree.active = new_node
        new_node.location = context.space_data.cursor_location[0]-new_node.width/2,context.space_data.cursor_location[1]
        bpy.ops.node.select_all(action='DESELECT')
        new_node.select = 1

        if not get_pref().quick_place:
            bpy.ops.transform.translate('INVOKE_DEFAULT')
        # self.node_enum_items(context)
        return {'FINISHED'}

    def invoke(self, context, event):

        context.window_manager.invoke_search_popup(self)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SearchAndLink)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SearchAndLink)
