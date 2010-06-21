from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='bibim',
      version=version,
      description="Bibtex Bibliography Index Maker",
      license='GPL',
      packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_dir={'':'src'},
      install_requires=['setuptools', 'simplejson', 'sqlalchemy'],
      entry_points="""
      # -*- Entry points: -*-
      """,
)

