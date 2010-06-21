
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

class Rater(object):
    """
    Abstract class that defines the necessary methods that have to be 
    implemented to rate RatedWrappers.
    """
    
    def rate(self, upvotes, downvotes):
        raise NotImplementedError
    

class AverageRater(Rater):
    def rate(self, upvotes, downvotes):
        if not (upvotes + downvotes):
            return 0.0
        return float(upvotes) / (upvotes + downvotes)
    
