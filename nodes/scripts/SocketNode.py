import bpy
from bpy.props import *
from ...node_tree import RenderStackNode

import socket as st


class RSNodeServerNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeServerNode'
    bl_label = 'Server'

    st.setdefaulttimeout(0)
    s = st.socket(st.AF_INET, st.SOCK_STREAM)

    on: BoolProperty(name='On', default=False)
    timeout: FloatProperty(name='Timeout', default=0.01)
    host: StringProperty(name='Host', default='localhost')
    msg: StringProperty(name='Msg', default='Hello RSN!')
    port: IntProperty(name='Port', default=2333)

    binded: BoolProperty(default=False)
    sended: BoolProperty(default=False)

    def init(self, context):
        self.width = 200
        self.s.setsockopt(st.SOL_SOCKET, st.SO_REUSEADDR, 1)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'on')
        layout.prop(self, 'host')
        layout.prop(self, 'msg')
        layout.prop(self, 'port')

        if self.on:
            self.execute(context)

    def remove(self, context):
        try:
            self.s.close()
        except:
            pass
        self.binded = False
        self.sended = False

    def execute(self, context):
        s = self.s
        try:
            try:
                clientsock, clientaddr = s.accept()
                clientsock.send(self.msg.encode())
                clientsock.settimeout(self.timeout)
                clientsock.close()
                self.sended = True
            except:
                s.setsockopt(st.SOL_SOCKET, st.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.listen(0)
                self.binded = True
        except:
            pass

        print(self.binded, self.sended)


class RSNodeClientNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeClientNode'
    bl_label = 'Client'

    on: BoolProperty(name='On', default=False)
    timeout: FloatProperty(name='Timeout', default=0.01)
    bufsize: IntProperty(name='bufsize', default=1024)
    host: StringProperty(name='Host', default='localhost')
    msg: StringProperty(name='Msg', default='Closed')
    port: IntProperty(name='Port', default=2333)

    st.setdefaulttimeout(0)
    s = st.socket(st.AF_INET, st.SOCK_STREAM)

    def init(self, context):
        self.width = 200
        self.s.setsockopt(st.SOL_SOCKET, st.SO_REUSEADDR, 1)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'on')
        layout.prop(self, 'timeout')
        layout.prop(self, 'bufsize')
        layout.prop(self, 'host')
        layout.prop(self, 'msg')
        layout.prop(self, 'port')

        if self.on:
            self.execute(context)

    def execute(self, context):
        try:
            st.setdefaulttimeout(self.timeout)
            c = st.socket(st.AF_INET, st.SOCK_STREAM)
            self.server = (self.host, self.port)
            c.connect(self.server)
            self.msg = c.recv(self.bufsize).decode()
            c.close()
            print(self.msg)
        except:
            pass


def register():
    bpy.utils.register_class(RSNodeServerNode)
    bpy.utils.register_class(RSNodeClientNode)
    bpy.types.WindowManager.rsn_serve_modal = bpy.props.BoolProperty(name='Running rsn server', default=False)


def unregister():
    bpy.utils.unregister_class(RSNodeServerNode)
    bpy.utils.unregister_class(RSNodeClientNode)
    del bpy.types.WindowManager.rsn_serve_modal
