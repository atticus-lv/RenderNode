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
        description="The SMTP Password for your receiver email",
        subtype='PASSWORD')


class NodeViewerProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")
    timer: FloatProperty(name='Update time (second)', default=0.05, min=0.01, max=0.5, step=1)


class RSN_Preference(bpy.types.AddonPreferences):
    bl_idname = __package__

    option: EnumProperty(items=[
        ('PROPERTIES', 'Properties', ''),
        ('NODES', 'Nodes', '')],
        default='NODES')

    log_level: EnumProperty(items=[
        ('10', 'Debug', ''),
        ('20', 'Info', ''),
        ('30', 'Warning', ''),
        ('40', 'Error', '')
    ], default='30')

    file_path_separator:EnumProperty(items=[
        ('.', 'Dot', ''),
        ('_', 'Underscore', ''),
        (' ', 'Space', ''),
    ], default='.')

    node_smtp: PointerProperty(type=NodeSmtpProps)
    node_viewer: PointerProperty(type=NodeViewerProps)

    update_scripts: BoolProperty(name='Update scripts nodes',
                                 description="Update scripts nodes when using viewer node to auto update")

    def draw_nodes(self):
        layout = self.layout

        col = layout.column(align=1)
        box = col.box().split().column(align=1)
        box.prop(self.node_smtp, 'show', text="SMTP Email Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_smtp.show else 'TRIA_RIGHT')
        if self.node_smtp.show:
            box.use_property_split = True
            box.prop(self.node_smtp, "server", text='Server')
            box.prop(self.node_smtp, "password", text='Password')

        col.separator(factor=0.2)
        box = col.box().split().column(align=1)
        box.prop(self.node_viewer, 'show', text="Viewer Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_viewer.show else 'TRIA_RIGHT')
        if self.node_viewer.show:
            box.use_property_split = True
            box.prop(self.node_viewer, 'timer', slider=1)
            box.prop(self, 'update_scripts')

    def draw_properties(self):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, 'log_level', text='Log')
        row = layout.row(align = 1)
        row.prop(self, 'file_path_separator', text='File Path Separator')

    def draw(self, context):
        row = self.layout.row(align=1)
        row.prop(self, "option", expand=1)
        if self.option == "PROPERTIES":
            self.draw_properties()
        elif self.option == "NODES":
            self.draw_nodes()


addon_keymaps = []


def add_keybind():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # viewer node
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('rsn.add_viewer_node', 'V', 'PRESS')
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('rsn.mute_nodes', 'M', 'PRESS')
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS')
        kmi.properties.name = "RSN_MT_PieMenu"
        addon_keymaps.append((km, kmi))

def remove_keybind():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def register():
    bpy.utils.register_class(NodeSmtpProps)
    bpy.utils.register_class(NodeViewerProps)
    bpy.utils.register_class(RSN_Preference)
    add_keybind()


def unregister():
    bpy.utils.unregister_class(RSN_Preference)
    bpy.utils.unregister_class(NodeViewerProps)
    bpy.utils.unregister_class(NodeSmtpProps)
    remove_keybind()
