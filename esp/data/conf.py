SSID = '[ssid]'
PASSWORD = '[pass]'
CONNECT_RETRIES = 10
CONNECTION_TIME = 6.0

ERROR_LOG_FILENAME = 'error.log'

TEMPLATE_FOLDER = 'server/templates/'

try:
    from .local_conf import *
except ImportError:
    pass
