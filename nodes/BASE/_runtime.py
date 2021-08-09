'''
This update system comes from rigging_nodes
Link: https://gitlab.com/AquaticNightmare/rigging_nodes
It is suitable for some internal value process (Such like the math node)
So RenderNode now can execute some complex operate
'''

# CACHE
#################

# cache last execute nodes for drawing
cache_executed_nodes = list()
# cache links
cache_socket_links = dict()
# cache node's dependants
cache_node_dependants = dict()
# cache socket values
cache_socket_variables = dict()
# cache group outputs
cache_node_group_outputs = dict()

# cache times
cache_node_times = dict()
cache_nodetree_times = dict()

# runtime, for heavy execute when updating
runtime_info = {
    'updating': False,
    'executing': False,
}

# LOG
##################
import logging

LOG_FORMAT = "RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')

import time


class MeasureTime():
    '''Class to use with the "with" statement that logs the times of execution for the given node'''

    def __init__(self, node, name):
        self.node = node
        self.name = name

    def __enter__(self):
        self.start_time = time.perf_counter_ns()

    def __exit__(self, type, value, traceback):
        end_time = time.perf_counter_ns()
        # get time nanosecond
        total_time = (float((end_time - self.start_time))) / 1000000000

        node_dict = cache_node_times.setdefault(self.node.id_data, {}).setdefault(self.node, {})

        if self.name in {'Execution'}:
            if self.name in cache_nodetree_times:
                cache_nodetree_times[self.name] += total_time
            else:
                cache_nodetree_times[self.name] = total_time

        if self.name in node_dict:
            node_dict[self.name] += total_time
        else:
            node_dict[self.name] = total_time
