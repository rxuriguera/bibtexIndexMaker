from setuptools import setup, find_packages, use_setuptools
use_setuptools(version='0.6c11')
setup(
    # basic package data
    name = "TestApp",
    version = "0.0",
    # package structure
    packages=find_packages('source'),
    package_dir={'':'source'},
    entry_points = {
    'console_scripts': [
            'testApp = bimaker.app:main'
            ]
    },
)
