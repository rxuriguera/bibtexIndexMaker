
# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker. 
#
# BibtexIndexMaker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BibtexIndexMaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BibtexIndexMaker. If not, see <http://www.gnu.org/licenses/>.



from logging import config #@UnresolvedImport
from logging import getLogger #@UnresolvedImport
from os import path

# Logging
config.fileConfig(
    path.normpath(path.join(path.dirname(__file__),
                            '../../config/logging.cfg')))
log = getLogger('bibim')

# Config File
bibim_config = path.normpath(path.join(path.dirname(__file__),
                                       '../../config/bibim.cfg'))
if not path.exists(bibim_config):
    raise ValueError('Could not read configuration file (%s)' % bibim_config)
