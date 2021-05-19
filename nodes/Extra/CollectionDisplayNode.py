import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeCollectionDisplayNode(RenderStackNode):
    bl_idname = 'RSNodeCollectionDisplayNode'
    bl_label = 'Collection Display'

    collection: PointerProperty(type=bpy.types.Collection, name='Collection', update=update_node)
    hide_viewport: BoolProperty(name='Hide Viewport', default=False, update=update_node)
    hide_render: BoolProperty(name='Hide Render', default=False, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)

        row = col.row(align=1)
        row.prop(self, "collection", text='')

        row.prop(self, 'hide_viewport', text='',
                 icon='HIDE_OFF' if not self.hide_viewport else 'HIDE_ON')
        row.prop(self, 'hide_render', text='',
                 icon='RESTRICT_RENDER_OFF' if not self.hide_render else 'RESTRICT_RENDER_ON')

    def get_data(self):
        task_data_obj = {}
        if self.collection:
            task_data_obj[self.name] = {'collection'   : f"bpy.data.collections['{self.collection.name}']",
                                        'hide_viewport': self.hide_viewport,
                                        'hide_render'  : self.hide_render}

        return task_data_obj


def register():
    bpy.utils.register_class(RSNodeCollectionDisplayNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCollectionDisplayNode)
