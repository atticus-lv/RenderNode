import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode

import socket


class RSN_OT_SetUpServer(bpy.types.Operator):
    bl_idname = 'rsn.set_up_server'
    bl_label = 'Set Up Server (Not ready yet)'

    port: IntProperty(name='Port', default=2333)

    server = None
    conn = None
    addr = None

    data = None

    def add_handler(self):
        self._timer = bpy.context.window_manager.event_timer_add(0.2, window=bpy.context.window)
        bpy.context.window_manager.modal_handler_add(self)

    def remove_handles(self):
        bpy.context.window_manager.event_timer_remove(self._timer)

    def modal(self, context, event):
        if event.type == 'TIMER':
            if context.window_manager.rsn_serve_modal == True:
                try:
                    data = self.conn.recv(1024)  # 接收数据
                    if data != self.data:
                        self.conn.send(data.upper())  # 然后再发送数据
                        self.data = data
                except ConnectionResetError as e:
                    print('Closed a busy link')
            else:
                self.remove_handles()
                self.conn.close()

        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.rsn_serve_modal = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 2333))
        self.server.listen(5)
        print(f'{self.name} Listening!')
        self.conn, self.addr = self.server.accept()

        self.add_handler()

        return {'RUNNING_MODAL'}


class RSNodeServerNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeServerNode'
    bl_label = 'Server'

    port: IntProperty(name='Port', default=2333)

    def init(self, context):
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, "port", expand=1)
        if not context.window_manager.rsn_serve_modal:
            layout.operator("rsn.set_up_server").port = self.port
        else:
            layout.prop(context.window_manager, "rsn_serve_modal", toggle=1)


def register():
    bpy.utils.register_class(RSNodeServerNode)
    bpy.utils.register_class(RSN_OT_SetUpServer)
    bpy.types.WindowManager.rsn_serve_modal = bpy.props.BoolProperty(name='Running rsn server', default=False)


def unregister():
    bpy.utils.unregister_class(RSNodeServerNode)
    bpy.utils.unregister_class(RSN_OT_SetUpServer)
    del bpy.types.WindowManager.rsn_serve_modal
