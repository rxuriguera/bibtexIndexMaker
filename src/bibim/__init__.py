import logging #@UnresolvedImport
import logging.config #@UnresolvedImport
from os import path

logging.config.fileConfig(
    path.normpath(path.join(path.dirname(__file__),
                            '../../config/logging.cfg')))

log = logging.getLogger('bibim')


bibim_config = path.normpath(path.join(path.dirname(__file__),
                                       '../../config/bibim.cfg'))
if not path.exists(bibim_config):
    raise ValueError('Could not read configuration file (%s)' % bibim_config)
