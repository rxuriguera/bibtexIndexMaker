
# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker.
#
# BibimConfig is largely based on AtomisatorConfig from the Atomisator project.
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

from ConfigParser import ConfigParser #@UnresolvedImport
import re

from bibim import bibim_config

class BibimConfig(object):

    def __init__(self):
        self._parser = ConfigParser()
        self._file = bibim_config
        self._parser.read([self._file])
    
    def _get_simple_field(self, section, field, default=None):
        """
        Returns an option located in the configuration file.
        """
        if not self._parser.has_option(section, field):
            return default
        return self._parser.get(section, field).strip()

    def _set_simple_field(self, section, field, value):
        """
        Set an option in the configuration file.
        """
        self._parser.set(section, field, value)

    def _set_multiline_value(self, section, name, value):
        """
        Set a multi-line option in the configuration file.
        """
        def _quote(value):
            if ' ' in value:
                value = value.replace('"', "'")
                return '"%s"' % value
            return value

        def _line(entry):
            main = entry[0]
            params = [_quote(e) for e in entry[1]]
            return '%s %s' % (main, ' '.join(params))

        values = '\n'.join([_line(v) for v in value])
        self._parser.set(section, name, values)

    def _get_multiline_value(self, section, name, default=None):
        """
        Returns a multi-line option located in the configuration file.
        """
        if not self._parser.has_option(section, name):
            return default is None and None or []
        lines = self._parser.get(section, name).split('\n')
        # crappy pattern matching
        def _rep(match):
            return match.groups()[0].replace(' ', ':::')
        def _args(line):
            line = re.sub(r'"(.*?)"', _rep, line)
            line = [element.replace(':::', ' ')
                    for element in line.split() if element != '']
            return line[0].strip(), tuple([el.strip() for el in line[1:]])
        return [_args(line) for line in lines if line.strip() != '']


    def _get_comma_separated_dictionary(self, section, name, default=None):
        """
        Returns a multi-value option located in the configuration file in the
        form of a dictionary
        """
        if not self._parser.has_option(section, name):
            return default is None and None or []
        lines = self._parser.get(section, name).split('\n')
        # crappy pattern matching
        def _rep(match):
            return match.groups()[0].replace(' ', ':::')
        def _args(line):
            line = re.sub(r'"(.*?)"', _rep, line)
            line = [element.replace(':::', ' ')
                    for element in line.split(',') if element != '']
            return line[0].strip(), tuple([el.strip() for el in line[1:]])
            
        values = {}
        for line in lines:
            if line.strip() == '':
                continue
            key, value = _args(line)
            values[key] = value
        
        return values
    
    def _get_validation_properties(self, section='wrappers', name='field_validation', default={}):
        """
        Returns a dictionary of tuples associated to fields
        """
        if not self._parser.has_option(section, name):
            return default is None and None or []
        lines = self._parser.get(section, name).split('\n')
        # crappy pattern matching
        def _rep(match):
            return match.groups()[0].replace(' ', ':::')
        def _args(line):
            line = re.sub(r'"(.*?)"', _rep, line)
            # Elements must be separated by semicolons in the configuration
            # file
            line = [element.replace(':::', ' ')
                    for element in line.split(';') if element != '']
            value_list = [float(line[1])]
            value_list.extend([el.strip() for el in line[2:]])
            return line[0].strip(), value_list
            
        values = {}
        for line in lines:
            if line.strip() == '':
                continue
            key, value = _args(line)
            values[key] = value
        
        return values
    
    def write(self):
        """
        Saves the configuration.
        Writes the configuration into the file provided at initialization.
        """
        file_ = open(self._file, 'w')
        try:
            self._parser.write(file_)
        except:
            file_.close()
            
    def _get_database(self):
        return self._get_simple_field('database', 'uri', 'sqlite:///_temp_.db')
    
    def _set_database(self, value):
        self._set_simple_field('database', 'uri', value)
    
    def _get_search_engine(self):
        return int(self._get_simple_field('search', 'engine', 0))
    
    def _get_search_properties(self):
        properties = {}
        properties['min_query_length'] = (
            int(self._get_simple_field('search', 'min_query_length', 6)))
        properties['max_query_length'] = (
            int(self._get_simple_field('search', 'max_query_length', 10)))
        properties['queries_to_skip'] = (
            int(self._get_simple_field('search', 'queries_to_skip', 3)))
        properties['max_queries_to_try'] = (
            int(self._get_simple_field('search', 'max_queries_to_try', 5)))
        properties['too_many_results'] = (
            int(self._get_simple_field('search', 'too_many_results', 25)))
        return properties
    
    def _get_wrapper_properties(self):
        properties = {}
        properties['max_wrappers'] = (
            int(self._get_simple_field('wrappers', 'max_wrappers', 50)))
        properties['field_validation'] = (
            self._get_validation_properties())
        properties['min_validity'] = (
            float(self._get_simple_field('wrappers', 'min_validity', 0.7))) 
        properties['wrapper_gen_examples'] = (
            int(self._get_simple_field('wrappers', 'wrapper_gen_examples', 2)))
        properties['max_examples_from_db'] = (
            int(self._get_simple_field('wrappers', 'max_examples_from_db',
                                       15)))  
        properties['max_examples'] = (
            int(self._get_simple_field('wrappers', 'max_examples', 5)))
        properties['seconds_between_requests'] = (
            float(self._get_simple_field('wrappers',
                                         'seconds_between_requests', 5.0)))                 
        return properties
    
    def _get_black_list(self):
        black_list = self._get_multiline_value('search', 'black_list')
        # Remove any args
        return [tuple[0] for tuple in black_list]
        
    
    database = property(_get_database, _set_database)
    search_engine = property(_get_search_engine)
    search_properties = property(_get_search_properties)
    wrapper_properties = property(_get_wrapper_properties)
    black_list = property(_get_black_list)

# The rest of modules will export the configuration object. This way, we'll
# only have one instance of BibimConfig.
configuration = BibimConfig()
        
