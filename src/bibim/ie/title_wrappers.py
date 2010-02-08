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


from bibim.ie.wrappers import FieldWrapper


class TitleFieldWrapper(FieldWrapper):
    """
    The methods of this class try to extract the title of a given page.
    """
    
    _shortcuts = {
        'portal.acm.org':'_do_title_tag'
    }

    def _do_title_tag(self, page):
        title = page.find('title')
        if not title:
            return None
        text = title.find(text=True)
        return text
    
    def _do_strong_in_colspan_td(self, page):
        strong = text = None
        tds = page.findAll('td', {'colspan':True})
        for td in tds:
            strong = td.find('strong')
            if strong:
                break
        if strong:
            text = strong.find(text=True)
        return text
