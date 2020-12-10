import bpy
from bpy.props import BoolProperty


class RSN_OT_CreatCompositorNode(bpy.types.Operator):
    bl_idname = "rsn.creat_compositor_node"
    bl_label = "Separate Passes"

    remove: BoolProperty(default=False)

    def execute(self, context):
        scn = context.scene
        scn.use_nodes = True

        nt = context.scene.node_tree
        if "RSN Render Layers" in nt.nodes:
            render_layer_node = nt.nodes['RSN Render Layers']
        else:
            render_layer_node = nt.nodes.new(type="CompositorNodeRLayers")
            render_layer_node.name = 'RSN Render Layers'

        try:
            nt.nodes.remove(nt.nodes['RSN Output'])
        except:pass

        if not self.remove:
            file_output_node = nt.nodes.new(type="CompositorNodeOutputFile")
            file_output_node.name = "RSN Output"
            file_output_node.label = f"RSN Output"

            file_output_node.location = (300, 100)
            file_output_node.width = 200
            file_output_node.hide = True

            nt = context.scene.node_tree

            for i, output in enumerate(render_layer_node.outputs):
                name = output.name
                output_name = f"{name}/{name}_"
                if output_name not in file_output_node.file_slots:
                    file_output_node.file_slots.new(name=output_name)
                nt.links.new(render_layer_node.outputs[name], file_output_node.inputs[output_name])

        return {"FINISHED"}

def register():
    bpy.utils.register_class(RSN_OT_CreatCompositorNode)


def unregister():
    bpy.utils.unregister_class(RSN_OT_CreatCompositorNode)