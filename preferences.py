import bpy
from bpy.props import *

import rna_keymap_ui


class NodeSmtpProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")
    server: StringProperty(
        name="SMTP Server",
        description="Something Like 'smtp.qq.com' or 'smtp.gmail.com'",
        default="")

    password: StringProperty(
        name="SMTP Password",
        description="The SMTP Password for your receiver email", )


class NodeViewerProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")
    timer: FloatProperty(name='Update time (second)', default=0.2, min=0.1, max=2.0, step=10)


class RSN_Preference(bpy.types.AddonPreferences):
    bl_idname = __package__

    option: EnumProperty(items=[
        ('PROPERTIES', 'Properties', ''), ('NODES', 'Nodes', '')],
        default='PROPERTIES')

    node_smtp: PointerProperty(type=NodeSmtpProps)
    node_viewer: PointerProperty(type=NodeViewerProps)

    def draw_nodes(self):
        layout = self.layout
        layout.alignment = 'LEFT'

        col = layout.column(align=1)
        box = col.box().split().column(align=1)
        box.prop(self.node_smtp, 'show', text="SMTP Email Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_smtp.show else 'TRIA_RIGHT')
        if self.node_smtp.show:
            box.prop(self.node_smtp, "server", text='Server')
            box.prop(self.node_smtp, "password", text='Password')

        col.separator(factor=0.2)
        box = col.box().split().column(align=1)
        box.prop(self.node_viewer, 'show', text="Viewer Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_viewer.show else 'TRIA_RIGHT')
        if self.node_viewer.show:
            box.prop(self.node_viewer, 'timer')

    def draw_properties(self):
        pass

    def draw(self, context):
        row = self.layout.row(align=1)
        row.prop(self, "option", expand=1)
        if self.option == "PROPERTIES":
            self.draw_properties()
        elif self.option == "NODES":
            self.draw_nodes()





def register():
    bpy.utils.register_class(NodeSmtpProps)
    bpy.utils.register_class(NodeViewerProps)
    bpy.utils.register_class(RSN_Preference)




def unregister():


    bpy.utils.unregister_class(RSN_Preference)
    bpy.utils.unregister_class(NodeViewerProps)
    bpy.utils.unregister_class(NodeSmtpProps)
