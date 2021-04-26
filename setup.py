#!/usr/bin/env python3

import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-backup',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to conduct Web-based polls.',
    long_description=README,
    url='',
    author='phpusr',
    author_email='phpusr@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
