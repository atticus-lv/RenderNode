import json
import os
import logging
import time
import re
import numpy as np

from itertools import groupby
from collections import deque
from functools import lru_cache, wraps

import bpy
from mathutils import Color, Vector

from .preferences import get_pref

# init logger
LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')


def source_attr(src_obj, scr_data_path):
    def get_obj_and_attr(obj, data_path):
        path = data_path.split('.')
        if len(path) == 1:
            return obj, path[0]
        else:
            back_obj = getattr(obj, path[0])
            back_path = '.'.join(path[1:])
            return get_obj_and_attr(back_obj, back_path)

    return get_obj_and_attr(src_obj, scr_data_path)


def compare(obj: object, attr: str, val):
    """Use for compare and apply attribute since some properties change may cause depsgraph changes"""
    try:
        if getattr(obj, attr) != val:
            setattr(obj, attr, val)
            logger.debug(f'Attribute "{attr}" SET “{val}”')
    except AttributeError as e:
        logger.info(e)


class RenderQueueV2():
    def __init__(self, ntree, render_list_node):
        """init a rsn queue
        :parm ntree: a blender node tree(rsn node tree)
        :parm render_list_node: render_list_node

        """
        self.nt = ntree
        self.root_node = render_list_node
        self.mode = render_list_node.mode

        self.index_list = deque()
        self.task_dict_list = deque()

        self.init_queue()

    def init_queue(self):
        if self.mode == 'RANGE':
            input = self.root_node.inputs[0]
            if not input.is_linked: return

            task_info = input.get_value()
            print(task_info)
            if not task_info: return

            for i in range(self.root_node.range_start, self.root_node.range_end + 1):
                self.index_list.append(i)

        elif self.mode == 'STATIC':
            count = 0
            for i, input in enumerate(self.root_node.inputs):
                if not input.is_linked: continue
                self.index_list.append(i)

    @property
    def index(self):
        if not self.is_empty(): return self.index_list[0]

    @property
    def task_info(self):
        if not self.is_empty(): return self.task_dict_list[0]

    def force_update(self):
        if not self.is_empty():
            self.root_node.active_index = self.index_list[0]
            self.root_node.execute_tree()

    def is_empty(self):
        return len(self.index_list) == 0

    def pop(self):
        if not self.is_empty():
            return self.index_list.popleft()

    def clear_queue(self):
        self.task_dict_list.clear()
        self.index_list.clear()
