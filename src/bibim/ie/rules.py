
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

import re
import difflib #@UnresolvedImport

from bibim import log
from bibim.ie.types import Rule, Example
from bibim.references.util import split_name 

# TODO: Load these values from the configuration file
MINIMUM_RATIO = 0.5 
SIMILARITY_THRESHOLD = 0.8
MAX_SEPARATOR_CHARS = 10
MAX_REGEX_PATTERN_LEN = 40
MAX_CONTENT_ELEMENTS = 15


class DummyRule(Rule):
    def __init__(self, pattern=[]):
        log.debug('Applying DummyRule') #@UndefinedVariable
        super(DummyRule, self).__init__(pattern)
        
    def apply(self, input):
        return input


class PersonRule(Rule):
    """
    Defines how to convert a string to a person name. It expects a list of 
    names and returns a list of dictionaries.
    """
    def __init__(self, pattern=None):
        super(PersonRule, self).__init__('')
        
    def apply(self, input):
        log.debug('Applying PersonRule') #@UndefinedVariable
        if not type(input) == list:
            return []
        
        names = []
        for person in input:
            person = re.sub('\d', '', person)
            name = split_name(person)
            if name:
                names.append(name)
        return names
            

class RegexRule(Rule):
    """
    Defines how to apply a regex rule. The input must be a string and it will
    output a tuple with all the matching groups 
    """
    def apply(self, input):
        log.debug('Applying RegexRule with pattern %s' % self.pattern) #@UndefinedVariable
        regex = re.compile(self.pattern)
        
        try:
            input = input.strip()
            matches = re.match(regex, input)
        except Exception, e:
            log.error('Exception applying RegexRule with pattern %s: %s'  #@UndefinedVariable
                      % (self.pattern, e))
            return ''
        
        if matches and len(matches.groups()) > 0:
            return matches.group(1)
        else: 
            return ''


class MultiValueRegexRule(Rule):
    def apply(self, input):
        log.debug('Applying MultiValueRegexRule') #@UndefinedVariable
        results = []
        regex = re.compile(self.pattern)
        for string in input:
            matches = re.match(regex, string)
            if matches and len(matches.groups()) > 0:
                results.append(matches.group(1))
        return results
    

class SeparatorsRegexRule(MultiValueRegexRule):
    def apply(self, input):
        if type(input) == list:
            try:
                input = input[0]
            except IndexError, e:
                log.warn('Trying to apply SeparatorsRegexRule with empty list' #@UndefinedVariable
                         ' as input: %s' % e) 
                return input
        
        regex = [''.join([x, '|']) for x in self.pattern]
        regex = ''.join(regex)[:-1]
        
        return re.split(regex, input)


class PathRule(Rule):
    """
    Defines how to apply a path rule.
    The input of this rule must be a BeautifulSoup element and it will output
    a string.
    """
    def apply(self, input):
        log.debug('Applying PathRule') #@UndefinedVariable
        element = self._get_path_element(self.pattern, input)
        try:
            return element.find(name=True, text=True)
        except:
            return ''
    
    def _get_path_element(self, path, input):
        log.debug('Get path element for path: %s' % str(path)) #@UndefinedVariable
        # Make a local copy
        path = list(path)
        if not path:
            return None
        current = input
        tag, attrs, sibling = path.pop(0)
        
        # First element from the path must be unique
        elements = current.findAll(tag, attrs)
        if len(elements) != 1:
            return None
        current = elements[0]
        
        for tag, attrs, sibling in path:
            try:
                if sibling >= 0:
                    current = current.contents[sibling]
                else:
                    current = current.find(name=tag, attrs=attrs)
            except:
                current = None
                break
        return current


class MultiValuePathRule(Rule):
    """
    Defines how to apply a path rule that returns multiple values.
    The input of this rule must be a BeautifulSoup element and it will output
    a list of strings.
    """
    def apply(self, input):
        log.debug('Applying MultiValuePathRule') #@UndefinedVariable
        values = []
        elements = self._get_path_elements(self.pattern, input)
        for element in elements:
            try:
                text = ''.join(element.findAll(text=True))
                values.append(text) 
            except Exception, e:
                log.warn('MultiValuePathRule cannot find text for element ' #@UndefinedVariable
                         '%s: %s' % (str(element), e)) 
                continue
        return values
    
    def _get_path_elements(self, path, input):
        log.debug('Get path element for path: %s' % str(path)) #@UndefinedVariable
        # Make a local copy
        current = []
        path = list(path)
        if not path:
            return []
        tag, attrs, sibling = path.pop(0)
        
        # First element from the path must be unique
        elements = input.findAll(tag, attrs)
        if len(elements) != 1:
            return current
        current.append(elements[0])
        
        for tag, attrs, sibling in path:
            for index in range(len(current)):
                try:
                    if sibling is True:
                        elements = current[index].findAll(tag, attrs)
                        current[index] = elements.pop(0)
                        for element in elements:
                            current.append(element)
                    elif sibling >= 0:
                        current[index] = current[index].contents[sibling]
                except Exception, e:
                    log.warn('Error trying to get path element for path %s: %s' #@UndefinedVariable
                             % (str(path)[:50], e)) 
                    current[index] = None
                    break
        return current


class RuleFactory(object):
    def create_rule(self, rule_type, pattern):
        try:
            return globals()[rule_type](pattern)
        except KeyError:
            return Rule(pattern)

        
class Ruler(object):
    """
    Creates rules given a set of examples
    """
    def rule(self, training):
        """
        Given a set of examples, induces a rule that conforms them
        """
        # Make a local copy of training set
        training = list(training)
        if not training:
            return []
        
        rules = self._rule_example(training.pop())
        for example in training:
            example_rules = self._rule_example(example)
            self._merge_rules(rules, example_rules)
        return rules
 
    def _rule_example(self, example):
        """
        It creates a rule that works for a specific example 
        """
        return []
    
    def _merge_rules(self, generalized_rules, rules):
        """
        Given a list of rules, it finds their common with a list of some other
        rules. The result is a generalization covering the two collections. 
        """
        for rule in rules:
            self._merge_single_rule(generalized_rules, rule)
            
    def _merge_single_rule(self, g_rules, s_rule):
        """
        Given a rule and a list of rules, it generalizes the rules on the list
        so they cover the new case.
        """
        append_rule = True
        for g_rule in g_rules:
            if self._should_merge(g_rule, s_rule):
                g_rule.pattern = self._merge_patterns(g_rule.pattern,
                                                      s_rule.pattern)
                append_rule = False
                break
        if append_rule:
            g_rules.append(s_rule)
    
    
class RegexRuler(Ruler):
    """
    Creates rules consisting of a regular expression that can be used to
    extract a piece of information from a text.
    
    Content of the examples must be a string.
    """
    
    def _rule_example(self, example):
        log.debug('Ruling example with RegexRuler') #@UndefinedVariable
        try:
            text = example.content.strip()
        except Exception, e:
            log.warn('Error stripping %s: %s' % (str(example.content)[:40], e)) #@UndefinedVariable
            return []
        text = re.escape(text)
        pattern = text.replace(re.escape(example.value), '(.*)')
        
        if len(pattern) > MAX_REGEX_PATTERN_LEN:
            return []
        else:
            # In this case, only one rule is possible.
            return [RegexRule(pattern)]
    
    def _should_merge(self, g_rule, s_rule):
        sm = difflib.SequenceMatcher(None, g_rule.pattern, s_rule.pattern)
        return sm.quick_ratio() > SIMILARITY_THRESHOLD
    
    def _merge_patterns(self, g_pattern, s_pattern):
        log.debug('Merging RegexRuler patterns %s, %s' % #@UndefinedVariable
                  (g_pattern, s_pattern))
        
        sm = difflib.SequenceMatcher(None, g_pattern, s_pattern)
        while not sm.quick_ratio() == 1.0:
            matching_blocks = sm.get_matching_blocks()
            
            matching_blocks = self._apply_heuristics(g_pattern,
                                                     list(matching_blocks))
            
            g_pattern = self._replace_non_matching_block(g_pattern,
                                                         matching_blocks,
                                                         0)
            s_pattern = self._replace_non_matching_block(s_pattern,
                                                       matching_blocks,
                                                       1)
            
            while '(?:.*)(?:.*)' in g_pattern:
                g_pattern = g_pattern.replace('(?:.*)(?:.*)', '(?:.*)')
            while '(?:.*)(?:.*)' in s_pattern:
                s_pattern = s_pattern.replace('(?:.*)(?:.*)', '(?:.*)')
            
            log.debug('G_pattern: %s' % g_pattern) #@UndefinedVariable
            log.debug('S_pattern: %s' % s_pattern) #@UndefinedVariable
            
            sm.set_seqs(g_pattern, s_pattern)
        return g_pattern
    
    def _replace_non_matching_block(self, str, blocks, seq=0, block=0,
                                    rep='(?:.*)'):
        log.debug('Replacing non-matching blocks for pattern %s...' % str[:20]) #@UndefinedVariable
        # Check that the sequence is a or b
        if not ((seq in [0, 1]) and (len(blocks) > block)): 
            return ""
        
        if len(blocks) == block + 2:
            # Remove non-matching block
            start = blocks[block][seq]
            length = blocks[block][2]
            return str[start:start + length]
        else:
            start = blocks[block][seq] + blocks[block][2]
            length = blocks[block + 1][seq] - start
            return str[:start] + rep + str[start + length:]

    def _apply_heuristics(self, str, matching_blocks, seq=0):
        """
        This function applies an heuristic to remove matching blocks of length
        1 that are characters or numbers.
        It might be extended in the future
        """
        
        regex = re.compile("(\w{1})")
        length1 = [block for block in matching_blocks if block[2] == 1]
        
        for block in length1:
            char = str[block[seq]]
            matches = re.search(regex, char)
            if matches:
                matching_blocks.remove(block)
                
        return matching_blocks


class MultiValueRegexRuler(RegexRuler):
    def __init__(self):
        super(MultiValueRegexRuler, self).__init__()    
        self.parent_merge = super(MultiValueRegexRuler, self)._merge_patterns
        self.parent_should_merge = super(MultiValueRegexRuler,
                                         self)._should_merge
        
    def _escape(self, values, pattern):
        #pattern = re.escape(pattern)
        for value in values:
            pattern = re.sub(value, u'(.*)', pattern)
        return pattern     
       
class ElementsRegexRuler(MultiValueRegexRuler):
    """
    Creates rules consisting of a regular expression that can be used to
    extract a pieces of information from a text.
    
    Content of the examples must be a list of strings.
    """
    def __init__(self):
        super(ElementsRegexRuler, self).__init__()

    def _rule_example(self, example):
        log.debug('Ruling example with ElementsRegexRuler') #@UndefinedVariable
        content = list(example.content)
        if not content:
            return []
        
        g_pattern = self._escape(example.value, content.pop(0))        
        for element in content:
            s_pattern = self._escape(example.value, element)
            if self._should_merge(Rule(g_pattern), Rule(s_pattern)):
                g_pattern = self.parent_merge(g_pattern, s_pattern)
        return [MultiValueRegexRule(g_pattern)]
        
        
class SeparatorsRegexRuler(MultiValueRegexRuler):
    """
    Creates rules consisting of a regular expression that can be used to
    extract a pieces of information from a text.
    
    Content of the examples must be a string containing the values separated 
    by separators. (a single element list is also accepted)
    """
    def __init__(self):
        super(SeparatorsRegexRuler, self).__init__()
        
    def _rule_example(self, example):
        log.debug('Ruling example with SeparatorsRegexRuler') #@UndefinedVariable
        # Get example content
        if type(example.content) == list:
            content = list(example.content)
            if len(content) > 1:
                return [DummyRule()]
            else:
                content = content.pop()
        else:
            content = example.content
    
        g_pattern = self._escape(example.value, content)
        
        if g_pattern.count('(.*)') <= 1:
            return [DummyRule()]
        
        separators = self._find_separators(g_pattern)
        return [SeparatorsRegexRule(separators)]
    
    def _find_separators(self, pattern):
        raw_separators = [x for x in pattern.split('(.*)') 
                          if x and len(x) < MAX_SEPARATOR_CHARS]
         
        if not raw_separators:
            return []
         
        # If the string begins or ends with one of the separators of the raw
        # list, remove them
        if pattern.startswith(raw_separators[0]):
            raw_separators.pop(0)
        if pattern.endswith(raw_separators[-1]):
            raw_separators.pop()
        
        # Check again
        if not raw_separators:
            return []
        
        separators = self._merge_separators([raw_separators.pop(0)],
                                            raw_separators)
        return separators   

    def _merge_separators(self, separators, raw_separators):
        for separator in raw_separators:
            should_append = True
            for index in range(len(separators)): 
                if self.parent_should_merge(Rule(separators[index]),
                                      Rule(separator)):
                    separators[index] = self.parent_merge(separators[index],
                                                          separator)
                    should_append = False
                    break
            if should_append:
                separators.append(separator)
        return separators

    def _merge_patterns(self, g_pattern, s_pattern):
        return self._merge_separators(g_pattern, s_pattern)

    def _should_merge(self, g_rule, s_rule):
        return True
    

class PathRuler(Ruler):
    """
    Creates a rule described by the path to locate some piece of information 
    in an HTML document
    
    Content of the examples must be a BeautifulSoup object that describes an
    HTML document.
    """ 
    
    def _rule_example(self, example):
        log.debug('Ruling example with PathRuler. Value %s' % #@UndefinedVariable
                  str(example.value))
        rules = []
        element_rules = []
        for element in self._get_content_elements(example.value, example.content):
            rule = self._rule_element(example, element)
            if rule:
                element_rules.append(rule)
        self._merge_rules(rules, element_rules)
        return rules
    
    def _rule_element(self, example, element):
        try:
            pattern = self._get_element_path(example.content, element.parent)
            return PathRule(pattern)
        except Exception, e:
            log.warn('Path ruler cannot rule element %s: %s' #@UndefinedVariable 
                     % (str(element), e)) 
            return None
    
    def _get_content_elements(self, value, content):
        """
        Looks in the content to find the elements that contain the desired 
        value. Raises a ValueError exception if the content does not contain 
        the value.
        """
        try:
            elements = content.findAll(True, text=re.compile(value))
        except NameError, e:
            log.error("Example's content is not an HTML document: %s" % e) #@UndefinedVariable
            elements = []
        return elements[:MAX_CONTENT_ELEMENTS]

    def _should_merge(self, g_rule, s_rule):
        """
        Checks if the two patterns should be merged. In this case, two patterns
        should be merged if they have the same length with the same elements,
        i.e. they only differ in their attributes.
        """
        g_pattern, s_pattern = g_rule.pattern, s_rule.pattern
        should_merge = True
        if len(g_pattern) != len(s_pattern):
            should_merge = False
        
        for g_el, s_el in zip(g_pattern, s_pattern):
            if not (g_el[0] == s_el[0] and g_el[2] == s_el[2]):
                should_merge = False
                break
        
        return should_merge
    
    def _merge_patterns(self, g_pattern, s_pattern):
        """
        Merges two patterns (i.e. paths) of the same length and element names.
        """
        g_pattern = list(g_pattern)
        if not len(g_pattern) == len(s_pattern):
            raise ValueError
        
        for element01, element02 in zip(g_pattern, s_pattern):
            # Element attributes
            fields = {}
            for field in element01[1]:
                if ((field in element02[1]) and 
                    (element01[1][field] == element02[1][field])):
                    fields[field] = element01[1][field] 
            element01[1] = fields
        return g_pattern

    def _is_unique(self, document, description):
        """
        Test if there is more than one element with the given description 
        """
        elements = document.findAll(description[0], description[1])
        return (len(elements) == 1)

    def _get_element_attrs(self, element):
        """
        Returns the attributes of an element after doing some filtering.
        """
        forbidden_attrs = ['onclick', 'href', 'src']
        attrs = {}
        for name, value in element.attrs:
            if name not in forbidden_attrs:
                attrs[name] = value 
        return attrs
      
    def _get_sibling_number(self, element):
        parent = element.parent
        if not parent:
            return 0
        return parent.contents.index(element)
                
    def _get_element_description(self, element):
        return [element.name, self._get_element_attrs(element),
                self._get_sibling_number(element)]
        
    def _get_element_path(self, document, element):
        """
        Returns a unique path to the element. The path is composed by all the 
        necessary parent elements to make it unique. For each element it
        specifies: name, attributes and sibling number.
        Example:
            [[u'table', {u'width': u'100%'}, 7], [u'tr', {}, 0]]
        """
        path = []
        
        description = self._get_element_description(element)
        path.append(description)
        
        while not self._is_unique(document, description) and element:
            element = element.parent
    
            description = self._get_element_description(element)
            path.append(description)
        
        path.reverse()
        return path
  

class MultiValuePathRuler(PathRuler):
    """
    Creates a rule described by the path to locate various pieces of 
    information 
    in an HTML document
    
    Content of the examples must be a BeautifulSoup object that describes an
    HTML document.
    """ 
    
    def _rule_example(self, example):
        log.debug('Ruling example with MultiValuePathRuler') #@UndefinedVariable
        rule_example = super(MultiValuePathRuler, self)._rule_example
        values = list(example.value)
        count = len(values) 
        example_rules = []
        if not count:
            return []        
        
        # If there's only one value
        first_rules = rule_example(Example(values[0], example.content))
        if count == 1:
            for rule in first_rules:
                example_rules.append(MultiValuePathRule(rule.pattern))
            return example_rules
        
        more_rules = rule_example(Example(values[1], example.content))
        for f_rule in first_rules:
            f_rule_pattern = list(f_rule.pattern)
            if f_rule in more_rules:
                example_rules.append(MultiValuePathRule(f_rule_pattern))
                continue
            
            for s_rule in more_rules:
                s_rule_pattern = list(s_rule.pattern)
            
                # All should have same length
                if not len(f_rule_pattern) == len(s_rule_pattern):
                    continue
                
                # All should have same elements
                diff = False
                for element01, element02 in zip(f_rule_pattern, s_rule_pattern):
                    if element01[0] != element02[0]:
                        diff = True
                        break
                    elif element01[2] != element02[2]:
                        element01[2] = True
                    
                if diff:
                    continue
                example_rules.append(MultiValuePathRule(f_rule_pattern))
                
        return example_rules



class PersonRuler(Ruler):
    def rule(self, training):
        log.debug('Ruling with MultiValuePathRuler') #@UndefinedVariable
        return [PersonRule()]








