# import bpy
# from bpy.props import *
# from ...nodes.BASE.node_base import RenderNodeBase
#
#
# class RenderNodeSetCyclesLightPathsFastGI(RenderNodeBase):
#     """A simple input node"""
#     bl_idname = 'RenderNodeSetCyclesLightPathsFastGI'
#     bl_label = 'Set Cycles Light Paths FastGI'
#
#     def init(self, context):
#         self.create_input('RenderNodeSocketTask', 'task', 'Task')
#
#         self.create_input('RenderNodeSocketBool', 'use_fast_gi', 'Enable', default_value=False)
#         self.create_input('RenderNodeSocketFloat', 'ao_factor', 'AO Factor', default_value=1.0)
#         self.create_input('RenderNodeSocketFloat', 'ao_factor', 'AO Factor', default_value=1.0)
#
#         self.create_output('RenderNodeSocketTask', 'task', 'Task')
#
#     def process(self, context, id, path):
#         if not self.process_task(): return
#
#         for input in self.inputs:
#             key = input.name
#             value = input.get_value()
#             self.compare(bpy.context.scene.cycles, key, value)
#
#
# def register():
#     bpy.utils.register_class(RenderNodeSetCyclesLightPathsFastGI)
#
#
# def unregister():
#     bpy.utils.unregister_class(RenderNodeSetCyclesLightPathsFastGI)
