from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='bimaker.ir',
      version=version,
      description="BibtexIndexMaker package to retrieve information from the web",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='information retrieval bimaker',
      author='',
      author_email='',
      url='',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
