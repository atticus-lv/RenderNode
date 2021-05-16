import bpy


def draw_item(self, context):
    if context.area.ui_type == 'RenderStackNodeTree' and context.space_data and hasattr(context.space_data,
                                                                                        'node_tree'):

        self.layout.separator(factor=0.5)
        if context.scene.RSNBusyDrawing is True:
            self.layout.prop(context.scene, 'RSNBusyDrawing', text='Drawing...', toggle=1, icon='GREASEPENCIL')
        else:
            self.layout.operator("rsn.draw_nodes", icon='GREASEPENCIL')


def register():
    bpy.types.NODE_MT_editor_menus.append(draw_item)


def unregister():
    bpy.types.NODE_MT_editor_menus.remove(draw_item)
