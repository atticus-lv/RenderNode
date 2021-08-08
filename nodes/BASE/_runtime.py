# CACHE
#################
cache_socket_links = dict()

# cache current node's dependants
cache_node_dependants = dict()

# cache each value of the socket
cache_socket_variables = dict()

cache_node_group_outputs = dict()

cache_tree_portals = dict()

# runtime, for heavy execute when updating
runtime_info = {
    'updating': False,
    'executing': False,
}

# LOG
##################
import logging

LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')
