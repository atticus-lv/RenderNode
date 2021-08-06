import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


class RN_OT_AcceptUpdate(bpy.types.Operator):
    bl_idname = 'rsn.accept_update'
    bl_label = 'Accept Mode'

    _timer = None
    node_name: StringProperty()

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.node.accept_mode is False:
                context.window_manager.event_timer_remove(self._timer)
                return {"FINISHED"}
            else:
                self.node.store_data()
                ob = self.node.node_dict['object']
                if not ob:
                    return {'PASS_THROUGH'}
                if 'location' in self.node.inputs:
                    self.node.inputs['location'].value = ob.location
                if 'scale' in self.node.inputs:
                    self.node.inputs['scale'].value = ob.scale
                if 'rotation' in self.node.inputs:
                    self.node.inputs['rotation'].value = ob.rotation_euler

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.node = context.space_data.node_tree.nodes.get(self.node_name)
        if not self.node:
            return {'CANCELLED'}

        self.node.accept_mode = True
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}


def update_node(self, context):
    if self.use_p:
        self.creat_input('RenderNodeSocketTranslation', 'location', 'Location', default_value=(0, 0, 0))
    else:
        self.remove_input('location')

    if self.use_s:
        self.creat_input('RenderNodeSocketXYZ', 'scale', 'Scale', default_value=(1, 1, 1))
    else:
        self.remove_input('scale')

    if self.use_r:
        self.creat_input('RenderNodeSocketEuler', 'rotation', 'Rotation', default_value=(0, 0, 0))
    else:
        self.remove_input('rotation')

    if not self.accept_mode:
        self.update_parms()


class RenderNodeObjectPSR(RenderNodeBase):
    bl_idname = 'RenderNodeObjectPSR'
    bl_label = 'Object PSR'

    use_p: BoolProperty(name='P', update=update_node)
    use_s: BoolProperty(name='S', update=update_node)
    use_r: BoolProperty(name='R', update=update_node)

    accept_mode: BoolProperty(name='Accept Mode', default=False)

    def init(self, context):
        self.creat_input('RenderNodeSocketObject', 'object', 'Object')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        row = layout.split(factor=0.5)

        if self.accept_mode:
            row.prop(self, 'accept_mode', text='Accept', icon='IMPORT')
        else:
            row.operator('rsn.accept_update', icon='IMPORT', text='Accept').node_name = self.name

        sub = row.row(align=1)
        sub.prop(self, "use_p")
        sub.prop(self, "use_s")
        sub.prop(self, "use_r")

    def process(self):
        self.store_data()

        ob = self.node_dict['object']
        if not ob: return None

        if not self.accept_mode:

            if self.use_p: ob.location = self.node_dict['location']
            if self.use_s: ob.scale = self.node_dict['scale']
            if self.use_r: ob.rotation_euler = self.node_dict['rotation']


def register():
    bpy.utils.register_class(RN_OT_AcceptUpdate)
    bpy.utils.register_class(RenderNodeObjectPSR)


def unregister():
    bpy.utils.unregister_class(RN_OT_AcceptUpdate)
    bpy.utils.unregister_class(RenderNodeObjectPSR)
