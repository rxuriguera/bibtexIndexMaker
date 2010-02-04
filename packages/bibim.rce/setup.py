from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='bibim.rce',
      version=version,
      description="BibtexIndexMaker raw content extraction",
      license='GPL',
      packages = find_packages('src'),
      package_dir = {'':'src'},
      install_requires=['setuptools'],
      entry_points="""
      # -*- Entry points: -*-
      """,
)

