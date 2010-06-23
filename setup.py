import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
import glob
import platform #@UnresolvedImport
import sys, os

_tool_path_prefix = 'tools/xpdf/'
_tool_path = {
    'darwin':'linux/pdftotext', # MAC OS 
    'linux':'linux/pdftotext',
    'windows':'windows/pdftotext.exe'
}

platform = platform.system().lower()
if platform not in _tool_path.keys():
    tool = ''.join([_tool_path_prefix, 'linux'])
else:
    tool = ''.join([_tool_path_prefix, platform])
    
version = '0.0'

setup(name='bibim',
      version=version,
      description="Bibtex Bibliography Index Maker",
      license='GPL',
      keywords='bibtex pdf reference citation index ',
      url='http://github.com/rxuriguera/bibtexIndexMaker',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License (GPL)',
      ],
      packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests", "benchmark.*"]),
      package_dir={'':'src'},
      install_requires=['setuptools', 'simplejson', 'sqlalchemy'],
      include_package_data=True,
      data_files=[('config', glob.glob('config/*.cfg')),
                  (tool, glob.glob(''.join([tool, '/*'])))],
      entry_points={
        'gui_scripts': [
            'bibim = bibim.gui.main.main',
        ],
        'setuptools.installation': [
            'eggsecutable = bibim.gui.main:main',
        ]
    }
)
