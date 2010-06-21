
# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker.
#
# Session module is largely based on AtomisatorConfig from the Atomisator 
# project. 
# Copyright 2008 Tarek Ziade <tarek@ziade.org>
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

from sqlalchemy import create_engine #@UnresolvedImport
from sqlalchemy.orm import sessionmaker #@UnresolvedImport

from bibim.util.config import BibimConfig
from bibim.db.mappers import Base #@UnresolvedImport

metadata = Base.metadata #@UndefinedVariable
session = None

def create_session(sql_uri=BibimConfig().database, debug=False):
    """
    Creates a session.
    If 'global' is True creates a global session variable.
    """
    global session
    if not session or debug:
        engine = create_engine(sql_uri)
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine, autoflush=True, autocommit=True)
        session = Session()
    return session

def flush_changes():
    global session
    if not session:
        return
    session.flush()

if __name__ == '__main__':
    pass
