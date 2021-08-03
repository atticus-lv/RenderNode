
# CACHE
#################
cache_socket_links = dict()

# cache current node's dependants
cache_node_dependants = dict()

# runtime
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