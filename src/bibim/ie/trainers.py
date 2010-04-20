
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

from bibim.ie.examples import (Example, HTMLExampleManager)
from bibim.ie.rules import PathRuler, RegexRuler
from bibim.ie.wrappers import Wrapper

class TooFewExamplesError(Exception):
    pass


class WrapperTrainer(object):
    """
    This is a superclass for training ruled wrappers. 
    The given ExampleManager has to be compatible with the rulers in order
    for the trainer to work properly.
    The list of rulers must be ordered the same way as the rules will be 
    applied by the wrapper.
    """
    
    def __init__(self, example_manager, rulers=[], min=2):
        self.example_manager = example_manager
        self.rulers = rulers
        self.min_examples = min

    def get_example_manager(self):
        return self.__example_manager

    def get_rulers(self):
        return self.__rulers

    def get_min_examples(self):
        return self.__min_examples

    def set_example_manager(self, value):
        self.__example_manager = value

    def set_rulers(self, value):
        self.__rulers = value

    def set_min_examples(self, value):
        self.__min_examples = value

    example_manager = property(get_example_manager, set_example_manager)
    rulers = property(get_rulers, set_rulers)
    min_examples = property(get_min_examples, set_min_examples)     

    def train(self, examples):
        if len(examples) < self.min_examples:
            raise TooFewExamplesError
        wrappers = []
        rule_sets = self._get_rule_sets(list(self.rulers), examples)
        for set in rule_sets:
            wrappers.append(Wrapper())
        return wrappers
     
    def _get_rule_sets(self, rulers, example_set):
        if len(rulers):
            current_ruler = rulers.pop(0)
            new_rules = current_ruler.rule(example_set)
            new_rule_sets = []
            for rule in new_rules:
                current_example_set = self._get_new_example_set(rule,
                                                                example_set)
                rule_sets = self._get_rule_sets(list(rulers),
                                                current_example_set)
                map(lambda x: x.insert(0, rule), rule_sets)
                for rule_set in rule_sets:
                #    rule_set.insert(0, rule)
                    new_rule_sets.append(rule_set)
            return new_rule_sets
        else:
            return [[]]
        
    def _get_new_example_set(self, rule, example_set):
        """
        Return a list of examples with the same value attribute as example_set
        but where the content is the result of applying rule.
        """
        new_example_set = []
        for example in example_set:
            new_example_set.append(Example(example.value,
                                           rule.apply(example.content)))
        return new_example_set


class HTMLWrapperTrainer(WrapperTrainer):
    """
    This wrapper trainer will generate wrappers for HTML documents. These kind
    of documents need two rules: path rules and regex rules.
    """
    
    def __init__(self, min=2):
        super(HTMLWrapperTrainer, self).__init__(HTMLExampleManager(),
                                                 [PathRuler(), RegexRuler()],
                                                 min)
        
    def train(self, url):
        example_sets = self.example_manager.get_examples(url,
                                                         self.min_examples)
        return super(HTMLWrapperTrainer, self).train(example_sets)
        
