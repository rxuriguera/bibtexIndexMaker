
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

from bibim.ie.examples import HTMLExampleManager
from bibim.ie.rules import PathRuler, RegexRuler
from bibim.ie.wrappers import RuledWrapper

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
    
    def train(self, example_sets):   
        wrapper = RuledWrapper()     
        for set in example_sets:
            rules = self._train_field(example_sets[set])                    
            if rules:
                wrapper.add_field_rules(set, rules)
        return wrapper        

    def _train_field(self, examples):        
        if len(examples) < self.min_examples:
            raise TooFewExamplesError
        
        rules = []
        for ruler in self.rulers:
            rules.append(ruler.rule(examples))
        return rules


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
        
