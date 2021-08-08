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
                ob = self.node.inputs['object'].get_value()
                if not ob:
                    return {'PASS_THROUGH'}
                if 'location' in self.node.inputs:
                    self.node.inputs['location'].default_value = ob.location
                if 'scale' in self.node.inputs:
                    self.node.inputs['scale'].default_value = ob.scale
                if 'rotation' in self.node.inputs:
                    self.node.inputs['rotation'].default_value = ob.rotation_euler

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
        self.create_input('RenderNodeSocketTranslation', 'location', 'Location', default_value=(0, 0, 0))
    else:
        self.remove_input('location')

    if self.use_s:
        self.create_input('RenderNodeSocketXYZ', 'scale', 'Scale', default_value=(1, 1, 1))
    else:
        self.remove_input('scale')

    if self.use_r:
        self.create_input('RenderNodeSocketEuler', 'rotation', 'Rotation', default_value=(0, 0, 0))
    else:
        self.remove_input('rotation')

    if not self.accept_mode:
        self.update_parms()


class RenderNodeObjectPSR(RenderNodeBase):
    bl_idname = 'RenderNodeObjectPSR'
    bl_label = 'Object PSR'

    use_p: BoolProperty(name='Pos', update=update_node)
    use_s: BoolProperty(name='Scale', update=update_node)
    use_r: BoolProperty(name='Rotate', update=update_node)

    accept_mode: BoolProperty(name='Accept Mode', default=False)

    def init(self, context):
        self.create_input('RenderNodeSocketObject', 'object', '')
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.width = 200

    def draw_buttons(self, context, layout):
        sub = layout.row(align=1)
        sub.prop(self, "use_p")
        sub.prop(self, "use_s")
        sub.prop(self, "use_r")

        if self.accept_mode:
            layout.prop(self, 'accept_mode', text='Accept Mode', icon='IMPORT')
        else:
            layout.operator('rsn.accept_update', icon='IMPORT', text='Accept Mode').node_name = self.name

    def process(self):
        ob = self.inputs['object'].get_value()

        if ob and not self.accept_mode:
            if self.use_p: ob.location = self.inputs['location'].get_value()
            if self.use_s: ob.scale = self.inputs['scale'].get_value()
            if self.use_r: ob.rotation_euler = self.inputs['rotation'].get_value()


def register():
    bpy.utils.register_class(RN_OT_AcceptUpdate)
    bpy.utils.register_class(RenderNodeObjectPSR)


def unregister():
    bpy.utils.unregister_class(RN_OT_AcceptUpdate)
    bpy.utils.unregister_class(RenderNodeObjectPSR)
