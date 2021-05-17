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

        layout.prop(context.scene, 'rsn_bind_tree')

        if context.scene.rsn_bind_tree:
            box = layout.box().column(align=0)
            box.template_ID(context.scene, "rsn_bind_tree")

            row = box.row()
            row.operator('rsn.switch_to_bind_tree')

            pop = row.operator('rsn.pop_editor')
            pop.bind_tree = True
            pop.area_type = "NODE_EDITOR"


def scene_draw(self, context):
    RSN_PT_Panel.draw(self, context)


def poll_bind_tree(self, object):
    return object.bl_idname == 'RenderStackNodeTree'


def register():
    # bpy.types.Scene.bind_rsn_tree = StringProperty(name='Bind')
    bpy.types.Scene.rsn_bind_tree = PointerProperty(name='Render Tree', type=bpy.types.NodeTree, poll=poll_bind_tree)

    # bpy.utils.register_class(RSN_PT_Panel)
    bpy.types.SCENE_PT_scene.append(scene_draw)


def unregister():
    del bpy.types.Scene.rsn_bind_tree

    # bpy.utils.unregister_class(RSN_PT_Panel)
