import bpy
import os
import shutil

from bpy.props import *
from bpy.types import Operator, Menu, Panel
from bl_operators.presets import AddPresetBase
from bl_ui.utils import PresetPanel

from ...nodes.BASE.node_base import RenderNodeBase
from ... import __folder_name__


def update_node(self, context):
    self.execute_tree()


class RSNodeResolutionInputNode(RenderNodeBase):
    bl_idname = "RSNodeResolutionInputNode"
    bl_label = "Resolution"

    res_x: IntProperty(name="Resolution X", default=1920, min=4, subtype='PIXEL', update=update_node)
    res_y: IntProperty(name="Resolution Y", default=1080, min=4, subtype='PIXEL', update=update_node)
    res_scale: IntProperty(name="Resolution Scale", default=100, min=1, subtype='PERCENTAGE', soft_min=1, soft_max=100,
                           update=update_node)

    preset_mode: BoolProperty(name='Preset Mode', default=False)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        row = col.row(align=1)
        row.prop(self, 'res_x', text="X")
        row.prop(self, 'res_y', text="Y")
        col.prop(self, 'res_scale', text="%", slider=1)

        try:
            if hasattr(bpy.context.space_data, 'edit_tree'):
                if bpy.context.space_data.edit_tree.nodes.active.name == self.name:
                    row = layout.row(align=1)
                    if self.preset_mode:
                        row.popover(panel="RSN_PT_ResolutionPresetPanel", text="Resolution Preset",
                                    icon="PRESET")
                    else:
                        row.menu('RSN_MT_ResolutionPresetsMenu',icon = 'FULLSCREEN_EXIT')

                    row.prop(self, 'preset_mode',text='',icon='PRESET_NEW')

        except Exception:
            pass

    def get_data(self):
        task_data = {}
        task_data["res_x"] = self.res_x
        task_data['res_y'] = self.res_y
        task_data['res_scale'] = self.res_scale
        return task_data

    def apply_data(self, task_data):
        pass
        # if 'res_x' in task_data:
        #     rn = bpy.context.Scene.render
        #     self.compare(rn, 'resolution_x', task_data['res_x'])
        #     self.compare(rn, 'resolution_y', task_data['res_y'])
        #     self.compare(rn, 'resolution_percentage', task_data['res_scale'])


class RSN_MT_ResolutionPresetsMenu(Menu):
    bl_label = 'Resolution Preset'
    preset_subdir = 'RSN/resolution_preset'
    preset_operator = 'script.execute_preset'
    draw = Menu.draw_preset


class RSN_PT_ResolutionPresetPanel(PresetPanel, Panel):
    bl_label = 'RSN Resolution Presets'
    preset_subdir = 'RSN/resolution_preset'
    preset_operator = 'script.execute_preset'
    preset_add_operator = 'rsn.add_resolution_preset'


class RSN_OT_AddResolutionPreset(AddPresetBase, Operator):
    bl_idname = 'rsn.add_resolution_preset'
    bl_label = 'Add dict_input preset'
    preset_menu = 'SSM_MT_CamPresets'

    node_name: StringProperty(name='Node to add preset')
    # Common variable used for all preset values
    preset_defines = [
        'nt = bpy.context.space_data.edit_tree',
        'node = nt.nodes.active',
    ]

    preset_values = [
        'node.res_x',
        'node.res_y',
        'node.res_scale',
    ]

    preset_subdir = 'RSN/resolution_preset'


def get_files_from_path(path):
    files = []
    for dirName, subdirList, fileList in os.walk(path):
        dir_ = dirName.replace(path, '')
        for f in fileList:
            files.append(os.path.join(dir_, f))
    return files


def add_res_preset_to_user():
    presets_folder = bpy.utils.user_resource('SCRIPTS', "presets")
    rsn_presets_folder = os.path.join(presets_folder, 'RSN', 'resolution_preset')

    if not os.path.exists(rsn_presets_folder):
        os.makedirs(rsn_presets_folder, exist_ok=True)

    destination = get_files_from_path(rsn_presets_folder)

    addon_folder = bpy.utils.user_resource('SCRIPTS', "addons")

    bundled_presets_folder = os.path.join(addon_folder, __folder_name__, 'preset', 'resolution_preset')
    # Check what's in the add-on presets folder
    source = get_files_from_path(bundled_presets_folder)

    # Compare the folders
    difference = set(source) - set(destination)
    if len(difference) != 0:
        print('RSN will install bundled Resolution presets:\n' + str(difference))

    for f in difference:
        file = os.path.join(bundled_presets_folder, f)
        dest_file = os.path.join(rsn_presets_folder, f)
        dest_folder = os.path.dirname(dest_file)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder, exist_ok=True)

        shutil.copy2(file, dest_folder)


classes = (
    RSNodeResolutionInputNode,
    RSN_MT_ResolutionPresetsMenu,
    RSN_PT_ResolutionPresetPanel,
    RSN_OT_AddResolutionPreset
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    try:
        add_res_preset_to_user()
    except:
        pass

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
