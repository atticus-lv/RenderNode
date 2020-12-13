import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

import socket


class RSN_OT_ClientMsg(bpy.types.Operator):
    bl_idname = 'rsn.client_msg'
    bl_label = 'Send Message (Not ready yet)'

    port: IntProperty(name='Port', default=2333)
    msg: StringProperty(name='message', default="Message!")

    def execute(self, context):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', self.port))
        client.send(self.msg.encode('utf-8'))  # 发送一条信息 python3 只接收btye流
        data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
        print('recv:', data.decode())
        client.close()
        return {"FINISHED"}


class RSNodeClientNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeClientNode'
    bl_label = 'Client'

    port: IntProperty(name='Port', default=2333)
    msg:StringProperty(name='message', default="Message!")

    def init(self, context):
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, "port", expand=1)
        if not context.window_manager.rsn_serve_modal:
            layout.operator("rsn.client_msg").port = self.port
            layout.prop(self, "msg")



def register():
    bpy.utils.register_class(RSNodeClientNode)
    bpy.utils.register_class(RSN_OT_ClientMsg)


def unregister():
    bpy.utils.unregister_class(RSNodeClientNode)
    bpy.utils.unregister_class(RSN_OT_ClientMsg)