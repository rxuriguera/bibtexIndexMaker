import logging #@UnresolvedImport
import logging.config #@UnresolvedImport
from os import path

logging.config.fileConfig(
    path.normpath(path.join(path.dirname(__file__), '../../config/logging.cfg')))

log = logging.getLogger('bibim')
