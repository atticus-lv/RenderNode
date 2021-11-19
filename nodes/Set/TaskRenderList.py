import json

from bpy.props import *
from ...utility import *
from ...nodes.BASE.node_base import RenderNodeBase
from ...ui.icon_utils import RSN_Preview

from ..BASE._runtime import cache_node_dependants


def update_mode(self, context):
    if self.mode == 'RANGE':
        for i, input in enumerate(self.inputs):
            if i != 0:
                self.inputs.remove(input)
    else:
        self.auto_update_inputs('RenderNodeSocketTask', "Task")

    update_list(self, context)


def update_list(self, context):
    # set selector
    self.select_list.clear()
    if self.mode == 'STATIC':
        for i, input in enumerate(self.inputs):
            item = self.select_list.add()
            item.name = self.name
            item.index = i

    elif self.mode == 'RANGE':
        for i in range(self.range_start, self.range_end + 1):
            item = self.select_list.add()
            item.name = self.name
            item.index = i


def update_active_task(self, context):
    if not self.is_active_list: return
    # turn off others
    for node in self.id_data.nodes:
        if node.bl_idname == 'RenderNodeTaskRenderListNode' and node != self:
            node.is_active_list = False
    bpy.ops.rsn.draw_nodes('INVOKE_DEFAULT')
    context.area.tag_redraw()
    # execute
    context.window_manager.rsn_active_list = self.name
    context.scene.rsn_bind_tree = self.id_data  # bind tree
    self.execute_tree()


class RSN_OT_select_active_index(bpy.types.Operator):
    """Set Active"""
    bl_label = 'Select Active Index'
    bl_idname = 'rsn.select_active_index'

    node_name: StringProperty()
    index: IntProperty()

    def execute(self, context):
        node = context.space_data.node_tree.nodes[self.node_name]
        if hasattr(node, 'active_index'):
            try:
                setattr(node, 'active_index', self.index)
            except Exception as e:
                self.report({"ERROR"}, f'{e}')
        return {"FINISHED"}


class SelectorProperty(bpy.types.PropertyGroup):
    name: StringProperty(default="", name="List Node Name")
    index: IntProperty()  # real index
    color: FloatVectorProperty(name='Active Color', subtype='COLOR', default=(0, 5, 0), min=1, max=1)


class RSN_UL_SelectList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        nt = context.space_data.node_tree
        node = nt.nodes.get(item.name)
        if not node: return
        if item.index == node.active_index:
            c = layout.prop(item, 'color', text='')

        else:
            s = layout.operator('rsn.select_active_index', text=str(item.index))
            s.node_name = item.name
            s.index = item.index



class RenderNodeTaskRenderListNode(RenderNodeBase):
    """Render List Node"""
    bl_idname = 'RenderNodeTaskRenderListNode'
    bl_label = 'Task Render List'

    # task input mode
    mode: EnumProperty(name='Mode', items=[
        ('STATIC', 'Static', ''),
        ('RANGE', 'Range', ''),
    ], update=update_mode)

    # Range
    range_start: IntProperty(name='Range Start', update=update_list)
    range_end: IntProperty(name='Range End', update=update_list)

    # active set
    active_index: IntProperty(name="Active Index", min=0, update=update_active_task)
    is_active_list: BoolProperty(name="Active List", update=update_active_task)

    select_list: CollectionProperty(type=SelectorProperty)

    # active task ui

    # action after render
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='Clean filepath after render', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW',
        name='Display')

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'RenderStackNodeTree'}

    def init(self, context):
        self.width = 200

    def copy(self, node):
        self.is_active_list = False

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.prop(self, 'is_active_list')
        if not self.is_active_list: return

        render = box.operator('rsn.render_queue_v2', icon='SHADING_RENDERED')
        render.list_node_name = self.name

        box = layout.box()
        box.prop(self, 'mode')

        if self.mode == 'RANGE':
            col = box.column(align=True)
            col.prop(self, 'range_start')
            col.prop(self, 'range_end')

        layout.template_list(
            "RSN_UL_SelectList", "",
            self, "select_list",
            self, "active_index", type='GRID', columns=6, rows=5)


    def update(self):
        if self.mode == 'STATIC':
            self.auto_update_inputs('RenderNodeSocketTask', "task")

        update_list(self, bpy.context)

    def get_dependant_nodes(self):
        '''returns the nodes connected to the inputs of this node'''
        dep_tree = cache_node_dependants.setdefault(self.id_data, {})
        nodes = []

        if self.mode == 'STATIC':
            for index, input in enumerate(self.inputs):
                if index == self.active_index:
                    connected_socket = input.connected_socket
                    if connected_socket and connected_socket not in nodes:
                        nodes.append(connected_socket.node)
                    break


        else:
            connected_socket = self.inputs[0].connected_socket
            if connected_socket and connected_socket not in nodes:
                nodes.append(connected_socket.node)

        dep_tree[self] = nodes

        return nodes

    def process(self, context, id, path):
        value = self.process_task(index=self.active_index if self.mode == 'STATIC' else 0)

        if not value:
            return
        data = json.loads(value)

        context.scene.frame_start = data.get('frame_start')
        context.scene.frame_end = data.get('frame_end')
        context.scene.frame_step = data.get('frame_step')

        context.scene.render.filepath = data.get('filepath')




def register():
    bpy.utils.register_class(RSN_OT_select_active_index)
    bpy.utils.register_class(SelectorProperty)
    bpy.utils.register_class(RSN_UL_SelectList)
    bpy.utils.register_class(RenderNodeTaskRenderListNode)


def unregister():
    bpy.utils.unregister_class(RSN_OT_select_active_index)
    bpy.utils.unregister_class(SelectorProperty)
    bpy.utils.unregister_class(RSN_UL_SelectList)
    bpy.utils.unregister_class(RenderNodeTaskRenderListNode)
