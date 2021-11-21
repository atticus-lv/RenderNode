from ...nodes.BASE.node_base import RenderNodeBase
from ...preferences import get_pref

import bpy
from bpy.props import *


def test_email(self, context):
    if self.test_send:
        self.process()
        self.test_send = False


class RenderNodeEmailNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RenderNodeEmailNode'
    bl_label = 'Email'

    def init(self, context):
        self.create_input('RenderNodeSocketTask', 'task', 'Task')

        self.create_input('RenderNodeSocketBool', 'only_render', 'Send only in render mode')
        self.create_input('RenderNodeSocketString', 'subject', 'Subject')
        self.create_input('RenderNodeSocketString', 'content', 'Content')
        self.create_input('RenderNodeSocketString', 'sender_name', 'Sender Name')
        self.create_input('RenderNodeSocketString', 'email', 'Email')

        self.create_output('RenderNodeSocketTask', 'task', 'Task')

        self.width = 200

    def process(self, context, id, path):
        if not self.process_task(): return
        use = self.inputs['only_render'].get_value()
        if not use or (use and context.window_manager.rsn_running_modal):
            bpy.ops.rsn.send_email(subject=self.inputs['subject'].get_value(),
                                   content=self.inputs['content'].get_value(),
                                   sender_name=self.inputs['sender_name'].get_value(),
                                   email=self.inputs['email'].get_value())


def register():
    bpy.utils.register_class(RenderNodeEmailNode)


def unregister():
    bpy.utils.unregister_class(RenderNodeEmailNode)
