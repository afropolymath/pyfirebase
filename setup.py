#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='python-fire',
      version='1.0',
      description="Firebase Python Plugin",
      long_description="Built as an improvement on the python-firebase package built by ozgur",
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Natural Language :: English',
      ],
      keywords='firebase python python-fire',
      author='Chidiebere Nnadi',
      author_email='chidiebere.nnadi@gmail.com',
      maintainer='Chidiebere Nnadi',
      maintainer_email='chidiebere.nnadi@gmail.com',
      url='http://github.com/andela-cnnad/python-fire',
      license='MIT',
      packages=['pyfire'],
      test_suite='tests',
      tests_require=['pytest'],
      install_requires=['requests>=2.10.0', 'mock'],
      zip_safe=False,
      )
