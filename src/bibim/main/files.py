
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

import os.path

class FileManager(object):  
    def get_files_list(self, path, ext=None):
        path = os.path.normpath(path)
        self.check_path(path)
        files = []
        if os.path.isfile(path):
            files.append(unicode(path))
        elif os.path.isdir(path):
            if ext:
                files.extend(self.dir_entries(path, ext))
            else:
                files.extend(self.dir_entries(path))
        return files
        
    def check_path(self, path):
        if not os.access(path, os.W_OK):
            raise IOError('No access to path')
        
    def check_extension(self, path, ext):
        return path.endswith('.' + ext)

    def dir_entries(self, dir, *args):
        '''
        Return a list of file names found in directory 'dir'
        If there are no additional arguments, all files found in the directory 
        are added to the list.
        Example usage: fileList = dir_entries(r'/home', 'txt', 'py')
        Only files with 'txt' and 'py' extensions will be added to the list.
        Example usage: fileList = dir_entries(r'/home', True)
        All files and all the files in subdirectories under /home will be 
        added to the list.
        '''
        fileList = []
        for file in os.listdir(dir):
            dirfile = os.path.join(dir, file)
            dirfile = unicode(dirfile)
            if os.path.isfile(dirfile):
                if not args:
                    fileList.append(dirfile)
                else:
                    if os.path.splitext(dirfile)[1][1:] in args:
                        fileList.append(dirfile)
            elif os.path.isdir(dirfile):
                fileList.extend(self.dir_entries(dirfile, *args))
        return fileList

