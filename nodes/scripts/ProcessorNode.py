import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def process_bar(percent, total_length=15):
    bar = ''.join('|' * int(percent * total_length)) + f' %|100%'
    return bar


class RSNodeProcessorNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeProcessorNode'
    bl_label = 'Processor'

    ori_frame_list: IntProperty(default=1)
    curr_frame_list:IntProperty(default=1)

    c1:FloatVectorProperty(subtype='COLOR',default=(0,1,0))
    c2:FloatVectorProperty(subtype='COLOR',default=(1,0,0))

    def init(self, context):
        pass

    def draw_buttons(self, context, layout):
        layout.scale_y = 1.25

        layout.label(text=f"DONE / ALL :  {self.ori_frame_list - self.curr_frame_list} / {self.ori_frame_list}")
        percent =(self.ori_frame_list - self.curr_frame_list) / self.ori_frame_list
        row = layout.box().row(align =1)
        sub = row.split(factor= percent,align=1)
        sub.prop(self,'c1',text="")
        sub.prop(self,'c2',text="")
        row.label(text=f'{percent:.2%}')


def register():
    bpy.utils.register_class(RSNodeProcessorNode)


def unregister():
    bpy.utils.unregister_class(RSNodeProcessorNode)
