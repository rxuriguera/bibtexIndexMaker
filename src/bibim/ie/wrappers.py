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


class Wrapper(object):
    """
    Defines base methods that must be implemented by Wrappers. This is an
    abstract class.
    """
       
    def extract_info(self, source, page):
        """
        Given a source and a page, searches in the page for relevant
        information. This method must be implemented by a subclass.
        """
        raise NotImplementedError()
        
        
class FieldWrapper(Wrapper):
    """
    Allows concrete field extraction from semi-structured 
    """
    
    _shortcuts = {}
    
    def extract_info(self, source, page):
        """
        Extracts a field from the given page. Strategy: if the source is
        defined in the shortcuts list, it tries to extract relevant
        information with the given strategy.
        Otherwise, it tries with all available strategies. 
        """
        info = self._extract_with_shortcut(source, page)
        if info:
            return info
        
        strategies = [method for method in dir(self) if method.startswith('_do_')]
        for strategy in strategies:
            strategy = getattr(self, strategy)
            info = strategy(page)
            if info:
                break
        return info
 
    def _extract_with_shortcut(self, source, page):
        """
        Checks if there is a strategy defined for the given source. If so, it
        tries to extract information with it.
        """
        info = None
        if source in self._shortcuts.keys():
            x = self._shortcuts[source]
            strategy = getattr(self, x)
            info = strategy(page)
        return info
