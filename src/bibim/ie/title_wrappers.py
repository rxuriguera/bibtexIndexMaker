
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
        'portal.acm.org':'_do_title_tag',
        'www.springerlink.com':'_do_h2_in_td',
        'www.sciencedirect.com':'_do_div_with_class',
        'ieeexplore.ieee.org':'_do_title_tag',
        'citeseerx.ist.psu.edu':'_do_title_tag'
    }

    def _do_title_tag(self, page):
        # Some sites place the article title in the title tag, but with some
        # additional text that has to be removed
        to_remove = ['Welcome to IEEE Xplore 2.0: ', u'CiteSeerX \u2014 ']
        title = page.find('title')
        text = self._extract_text(title)
        if text:
            for string in to_remove:
                text = text.replace(string, "")                
        return text

    def _do_h2_in_td(self, page):
        tds = page.findAll('td')
        h2 = self._find_in('h2', tds)
        return self._extract_text(h2)
    
    def _do_strong_in_colspan_td(self, page):
        tds = page.findAll('td', {'colspan':True})
        strong = self._find_in('strong', tds)
        return self._extract_text(strong)

    def _do_div_with_class(self, page):
        class_name = {'articleTitle':True}
        div = page.find('div', {'class':class_name})
        return self._extract_text(div)

