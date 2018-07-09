#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='farmers',
      version='1.0',
      description='Farmer Market Management System',
      author='Abraham Cabrera',
      author_email='',
      url='',
      license="MIT",
      packages=find_packages(),
      install_requires=[
          "prettytable",
          "pymongo==3.7.0",
      ],
      entry_points={
          "console_scripts": [
               "farmers=farmers.cli:main",
          ]
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Office/Business',
          ],
     )