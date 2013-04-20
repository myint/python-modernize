#!/usr/bin/env python

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__),
                       'README.rst'), 'r') as readme:
    setup(
        name='modernize',
        author='Armin Ronacher',
        author_email='armin.ronacher@active-4.com',
        version='0.2.1',
        url='http://github.com/mitsuhiko/python-modernize',
        packages=['libmodernize', 'libmodernize.fixes'],
        description='A hack on top of 2to3 for modernizing code for '
                    'hybrid codebases.',
        long_description=readme.read(),
        scripts=['python-modernize'],
        zip_safe=False,
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7'
            'Programming Language :: Python :: 3.3'
        ]
    )
