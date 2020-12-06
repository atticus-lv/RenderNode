import bpy
from bpy.props import *


class RSN_Preference(bpy.types.AddonPreferences):
    bl_idname = __package__

    option: EnumProperty(items=[
        ('PROPERTIES', 'Properties', ''), ('NODES', 'Nodes', '')
    ],
        default='PROPERTIES'
    )

    smtp_server: StringProperty(
        name="SMTP Server",
        description="Something Like 'smtp.qq.com' or 'smtp.gmail.com'",
        default="")

    smtp_pass: StringProperty(
        name="SMTP Password",
        description="The SMTP Password for your receiver email", )

    viewer_timer: FloatProperty(name='Update time (second)', default=0.2, min=0.1, max=2.0,step=10)

    def draw_nodes(self):
        layout = self.layout
        box = layout.box().split().column(align=1)
        box.label(text="SMTP Email Node")
        box.prop(self, "smtp_server", text='Server')
        box.prop(self, "smtp_pass", text='Password')

        box = layout.box().split().column(align=1)
        box.label(text="Viewer Node")
        box.prop(self,'viewer_timer')

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
    bpy.utils.register_class(RSN_Preference)


def unregister():
    bpy.utils.unregister_class(RSN_Preference)
