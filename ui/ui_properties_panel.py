import bpy
from bpy.props import StringProperty, PointerProperty


class RSN_PT_Panel(bpy.types.Panel):
    bl_label = "Render Node"
    bl_idname = "RSN_PT_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "Scene"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=1)
        row.prop(context.scene, 'rsn_bind_tree')

        if context.scene.rsn_bind_tree:
            row.operator('rsn.switch_to_bind_tree', text='', icon='SCREEN_BACK')



def scene_draw(self, context):
    RSN_PT_Panel.draw(self, context)


def poll_bind_tree(self, object):
    return object.bl_idname == 'RenderNodeTree'


def register():
    # bpy.types.Scene.bind_rsn_tree = StringProperty(name='Bind')
    bpy.types.Scene.rsn_bind_tree = PointerProperty(name='Render Tree', type=bpy.types.NodeTree, poll=poll_bind_tree)

    # bpy.utils.register_class(RSN_PT_Panel)
    bpy.types.SCENE_PT_scene.append(scene_draw)


def unregister():
    del bpy.types.Scene.rsn_bind_tree

    # bpy.utils.unregister_class(RSN_PT_Panel)
