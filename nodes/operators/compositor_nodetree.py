import bpy
from bpy.props import BoolProperty, StringProperty
import os

from ...preferences import get_pref

class RSN_OT_CreatCompositorNode(bpy.types.Operator):
    bl_idname = "rsn.creat_compositor_node"
    bl_label = "Separate Passes"

    use_passes: BoolProperty(default=False)
    view_layer: StringProperty(default="")

    def set_context_layer(self):
        nt = bpy.context.scene.node_tree
        context_layer = None
        for node in bpy.context.scene.node_tree.nodes:
            if node.name == f'RSN {bpy.context.window.view_layer.name} Render Layers':
                context_layer = node
        if not context_layer:
            context_layer = nt.nodes.new(type="CompositorNodeRLayers")
            context_layer.name = f'RSN {bpy.context.window.view_layer.name} Render Layers'

        try:
            com = bpy.context.scene.node_tree.nodes['Composite']
            nt.links.new(context_layer.outputs[0], com.inputs[0])
        except Exception as e:
            self.report({"ERROR"}, 'No Composite Node Found(Check its name must be "Composite") ')

    def execute(self, context):
        scn = context.scene
        scn.use_nodes = True

        nt = context.scene.node_tree

        self.set_context_layer()

        try:
            render_layer_node = nt.nodes[f'RSN {self.view_layer} Render Layers']
        except:
            render_layer_node = nt.nodes.new(type="CompositorNodeRLayers")
            render_layer_node.name = f'RSN {self.view_layer} Render Layers'

        if self.view_layer != '':
            render_layer_node.layer = self.view_layer

        try:
            nt.nodes.remove(nt.nodes[f'RSN {self.view_layer} Output'])
        except Exception as e:
            pass

        if self.use_passes:
            file_output_node = nt.nodes.new(type="CompositorNodeOutputFile")
            file_output_node.name = f"RSN {self.view_layer} Output"
            file_output_node.label = f"RSN {self.view_layer} Output"

            file_output_node.base_path = os.path.join(context.scene.render.filepath, self.view_layer)
            file_output_node.location = (400, -300)
            file_output_node.width = 200
            file_output_node.hide = True

            nt = context.scene.node_tree

            pref = get_pref()
            separator = pref.file_path_separator

            for i, output in enumerate(render_layer_node.outputs):
                name = output.name
                output_name = f"{self.view_layer}{separator}{name}{separator}"
                if output_name not in file_output_node.file_slots:
                    file_output_node.file_slots.new(name=output_name)
                nt.links.new(render_layer_node.outputs[name], file_output_node.inputs[output_name])

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RSN_OT_CreatCompositorNode)


def unregister():
    bpy.utils.unregister_class(RSN_OT_CreatCompositorNode)
