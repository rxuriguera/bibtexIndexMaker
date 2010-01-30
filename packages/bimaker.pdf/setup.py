from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='bimaker.pdf',
      version=version,
      description="Bimaker PDF text extraction package",
      license='GPL',
      packages = find_packages('src'),
      package_dir = {'':'src'},
      install_requires=['setuptools'],
      entry_points="""
      # -*- Entry points: -*-
      """,
)

