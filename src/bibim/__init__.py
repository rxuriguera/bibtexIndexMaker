import logging
import logging.config
from os import path

logging.config.fileConfig(
    path.normpath(path.join(path.dirname(__file__), '../../config/logging.cfg')))

log = logging.getLogger('app')
