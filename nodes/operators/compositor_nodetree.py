import bpy
from bpy.props import BoolProperty, StringProperty


class RSN_OT_CreatCompositorNode(bpy.types.Operator):
    bl_idname = "rsn.creat_compositor_node"
    bl_label = "Separate Passes"

    use_passes: BoolProperty(default=False)
    view_layer: StringProperty(default="")

    def execute(self, context):
        scn = context.scene
        scn.use_nodes = True

        nt = context.scene.node_tree

        try:
            render_layer_node = nt.nodes[f'RSN {self.view_layer} Render Layers']
        except:
            render_layer_node = nt.nodes.new(type="CompositorNodeRLayers")
            render_layer_node.name = f'RSN {self.view_layer} Render Layers'

        if self.view_layer != '':
            render_layer_node.layer = self.view_layer

        try:
            nt.nodes.remove(nt.nodes[f'RSN {self.view_layer} Output'])
            # nt.nodes.remove(nt.nodes[f'Render Layers'])
        except:
            pass

        if self.use_passes:
            file_output_node = nt.nodes.new(type="CompositorNodeOutputFile")
            file_output_node.name = f"RSN {self.view_layer} Output"
            file_output_node.label = f"RSN {self.view_layer} Output"

            file_output_node.location = (400, -300)
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
