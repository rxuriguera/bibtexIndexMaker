
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

from math import ceil, floor

from bibim.ie.examples import HTMLExampleManager
from bibim.ie.rules import PathRuler, RegexRuler

class TooFewExamplesError(Exception):
    pass


class WrapperTrainer(object):
    def __init__(self, example_manager, rulers=[], tp=0.8, vp=0.2, min=2):
        self.example_manager = example_manager
        self.rulers = rulers
        self.training_percentage = tp
        self.validation_percentage = vp
        self.min_examples = min

    def get_example_manager(self):
        return self.__example_manager

    def get_rulers(self):
        return self.__rulers

    def get_training_percentage(self):
        return self.__training_percentage

    def get_validation_percentage(self):
        return self.__validation_percentage

    def get_min_examples(self):
        return self.__min_examples

    def set_example_manager(self, value):
        self.__example_manager = value

    def set_rulers(self, value):
        self.__rulers = value

    def set_training_percentage(self, value):
        self.__training_percentage = value

    def set_validation_percentage(self, value):
        self.__validation_percentage = value

    def set_min_examples(self, value):
        self.__min_examples = value

    example_manager = property(get_example_manager, set_example_manager)
    rulers = property(get_rulers, set_rulers)
    training_percentage = property(get_training_percentage, set_training_percentage)
    validation_percentage = property(get_validation_percentage, set_validation_percentage)
    min_examples = property(get_min_examples, set_min_examples)
    
    def train(self):
        raise NotImplementedError


class HTMLWrapperTrainer(WrapperTrainer):
    """
    This wrapper trainer will generate wrappers 
    """
    
    def __init__(self, tp=0.8, vp=0.2, min=2):
        super(HTMLWrapperTrainer, self).__init__(HTMLExampleManager(),
                                                 [PathRuler(), RegexRuler()],
                                                 tp, vp, min)
        
    def train(self, url):
        # HTMLExampleManager returns different sets of examples. We have 
        # to induce rules for each of them.
        example_sets = self.example_manager.get_examples(url, self.min_examples)
    
        for set in example_sets:
            training, validation = self._split_examples(example_sets[set])
            
            for ruler in self.rulers:
                rule = ruler.rule(training)
                
    
    def _split_examples(self, examples):
        """
        This method splits a set of examples into two: the training and 
        validation sets. It returns a list of two elements with the two sets
        of examples.
        """
        if len(examples) < self.min_examples:
            raise TooFewExamplesError
        
        training = list(examples)
        
        validation = set()
        validation_length = int(ceil(self.validation_percentage * 
                                     len(examples)))
        for i in range(validation_length): 
            validation.add(training.pop())
        
        return (training, validation)
    
