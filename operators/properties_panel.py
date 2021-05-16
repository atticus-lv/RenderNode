import bpy
from bpy.props import StringProperty, PointerProperty


class RSN_PT_Panel(bpy.types.Panel):
    bl_label = "Render Node"
    bl_idname = "RSN_PT_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, 'bind_rsn_tree')

        row = layout.row()

        row.operator('rsn.switch_to_bind_tree')

        pop = row.operator('rsn.pop_editor')
        pop.bind_tree = True
        pop.area_type = "NODE_EDITOR"


def poll_bind_tree(self, object):
    return object.bl_idname == 'RenderStackNodeTree'


def register():
    # bpy.types.Scene.bind_rsn_tree = StringProperty(name='Bind')
    bpy.types.Scene.bind_rsn_tree = PointerProperty(name='Bind', type=bpy.types.NodeTree, poll=poll_bind_tree)

    bpy.utils.register_class(RSN_PT_Panel)


def unregister():
    del bpy.types.Scene.bind_rsn_tree

    bpy.utils.unregister_class(RSN_PT_Panel)
