import bpy
import rna_keymap_ui
from bpy.props import *

from . import __folder_name__


def get_pref():
    return bpy.context.preferences.addons.get(__folder_name__).preferences


class PropsDrawNodes(bpy.types.PropertyGroup):
    text_color1: FloatVectorProperty(name='Time < 0.1ms Color', subtype='COLOR',
                                     default=(1, 1, 1))

    text_color2: FloatVectorProperty(name='Time > 0.1ms Color', subtype='COLOR',
                                     default=(0, 1, 0))

    text_color3: FloatVectorProperty(name='Time >1ms Color', subtype='COLOR',
                                     default=(1, 0, 0))


class NodeViewLayerPassedProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")

    comp_node_name: StringProperty(
        name="Composite node Name",
        description="Default Name of the Composite node",
        default="Composite")


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


class NodeFilePathProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")

    path_format: StringProperty(name='Default Path Format',
                                default='$blend_render/$V/$label.$camera.$F4')

    time_behaviour: EnumProperty(
        name='Time behaviour($T)',
        items=[
            ('TASK', 'By Task', ''),
            ('FRAME', 'By Frame', '')],
        default='TASK')


class RSN_Preference(bpy.types.AddonPreferences):
    bl_idname = __package__

    option: EnumProperty(items=[
        ('PROPERTIES', 'Properties', ''),
        ('NODES', 'Nodes', ''),
        ('KEYMAP', 'Keymap', ''), ],
        default='NODES')

    draw_nodes: PointerProperty(type=PropsDrawNodes)

    # Tab Search
    quick_place: BoolProperty(name="Quick Place",
                              description="When using the quick search to add nodes,quick place without moveing it",
                              default=False)
    limited_area: BoolProperty(name='Limited Area',
                               description='Limited RenderNode Helper only in Render Editor',
                               default=True)

    log_level: EnumProperty(name='Log Level',
                            items=[
                                ('10', 'Debug', ''),
                                ('20', 'Info', ''),
                                ('30', 'Warning', ''),
                                ('40', 'Error', '')],
                            default='30', )

    need_update: BoolProperty(name='Need Update')
    latest_version: IntProperty()

    node_view_layer_passes: PointerProperty(type=NodeViewLayerPassedProps)
    node_smtp: PointerProperty(type=NodeSmtpProps)
    node_file_path: PointerProperty(type=NodeFilePathProps)

    def draw(self, context):
        row = self.layout.row(align=1)
        row.prop(self, "option", expand=1)
        if self.option == "PROPERTIES":
            self.draw_properties()
        elif self.option == "NODES":
            self.draw_nodes_option()
        elif self.option == 'KEYMAP':
            self.drawKeymap()

    def draw_nodes_option(self):
        layout = self.layout
        col = layout.column(align=1)

        col.separator(factor=0.2)
        box = col.box().split().column(align=1)
        self.filepath_node(box)

        # col.separator(factor=0.2)
        # box = col.box().split().column(align=1)
        # self.view_layer_passes_node(box)
        #
        # col.separator(factor=0.2)
        # box = col.box().split().column(align=1)
        # self.smtp_node(box)

    def draw_properties(self):
        layout = self.layout
        layout.use_property_split = True

        layout = self.layout
        col = layout.column()

        box = col.box().split().column(align=1)
        box.label(text="RenderNode Helper", icon='HELP')
        box.prop(self, 'quick_place')
        box.prop(self, 'limited_area')

        box = col.box().split().column(align=1)
        box.label(text="Time Debug", icon='TIME')
        box.prop(self.draw_nodes, 'task_color')
        box.separator(factor=1)

        box.prop(self.draw_nodes, 'text_color1')
        box.prop(self.draw_nodes, 'text_color2')
        box.prop(self.draw_nodes, 'text_color3')

        layout.separator(factor=0.5)
        # TODO fix log level
        # layout.prop(self, 'log_level', text='Debug')

    def view_layer_passes_node(self, box):
        box.prop(self.node_view_layer_passes, 'show', text="View Layer Passes Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_view_layer_passes.show else 'TRIA_RIGHT')
        if self.node_view_layer_passes.show:
            box.use_property_split = True
            box.prop(self.node_view_layer_passes, "comp_node_name")

    def filepath_node(self, box):
        box.prop(self.node_file_path, 'show', text="Set File Path Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_file_path.show else 'TRIA_RIGHT')
        if not self.node_file_path.show: return

        box.use_property_split = True
        box.prop(self.node_file_path, "path_format")

        enum_path_exp = [
            ('', 'File', ''),
            ('$path', 'File Path', ''),
            ('$blend', 'File Name', ''),
            ('', 'Context', ''),
            ('$label', 'Task Label', ''),
            ('$engine', 'Render Engine', ''),
            ('$camera', 'Scene Camera', ''),
            ('$res_x', 'Resolution X', ''),
            ('$res_y', 'Resolution Y', ''),
            ('$ev', 'Exposure Value(Color Management)', ''),
            ('$vl', 'View Layer', ''),
            ('', 'Time', ''),
            ('$T{%m}', 'Date: month', ''),
            ('$T{%d}', 'Date: day', ''),
            ('$T{%H}', 'Time: hour', ''),
            ('$T{%M}', 'Time: minute', ''),
        ]
        box.label(text=f'Tips', icon="INFO")
        for path in enum_path_exp:
            if path[0] == '': continue
            row = box.row()
            row.alignment = "CENTER"
            row.separator()
            row.label(text=f'{path[0]}: {path[1]}')

    def smtp_node(self, box):
        box.prop(self.node_smtp, 'show', text="SMTP Email Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_smtp.show else 'TRIA_RIGHT')
        if self.node_smtp.show:
            box.use_property_split = True
            box.prop(self.node_smtp, "server", text='Server')
            box.prop(self.node_smtp, "password", text='Password')

    def drawKeymap(self):
        col = self.layout.box().column()
        # col.label(text="Keymap", icon="KEYINGSET")
        km = None
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        old_km_name = ""
        get_kmi_l = []

        for km_add, kmi_add in addon_keymaps:
            for km_con in kc.keymaps:
                if km_add.name == km_con.name:
                    km = km_con
                    break

            for kmi_con in km.keymap_items:
                if kmi_add.idname == kmi_con.idname and kmi_add.name == kmi_con.name:
                    get_kmi_l.append((km, kmi_con))

        get_kmi_l = sorted(set(get_kmi_l), key=get_kmi_l.index)

        for km, kmi in get_kmi_l:
            if not km.name == old_km_name:
                col.label(text=str(km.name), icon="DOT")

            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)

            old_km_name = km.name


addon_keymaps = []

classes = (
    PropsDrawNodes,

    NodeViewLayerPassedProps,
    NodeSmtpProps,
    NodeFilePathProps,
    # pref
    RSN_Preference,
)


def add_keybind():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        # viewer node
        kmi = km.keymap_items.new('rsn.set_active_list', 'V', 'PRESS')
        addon_keymaps.append((km, kmi))
        # copy
        kmi = km.keymap_items.new('rsn.copy_and_link', 'D', 'PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        # tab search
        kmi = km.keymap_items.new('rsn.search_and_link', 'TAB', 'PRESS')
        addon_keymaps.append((km, kmi))
        # mute node
        kmi = km.keymap_items.new('rsn.mute_nodes', 'M', 'PRESS')
        addon_keymaps.append((km, kmi))
        # helper pie
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS')
        kmi.properties.name = "RSN_MT_PieMenu"
        addon_keymaps.append((km, kmi))

        # group nodes
        kmi = km.keymap_items.new("rsn.group_nodes", 'G', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("rsn.edit_group", 'TAB', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))


def remove_keybind():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    add_keybind()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    remove_keybind()
