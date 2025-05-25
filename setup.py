#!/usr/bin/env python3

import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-backup',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A simple Django app to regular backup db to Google Drive.',
    long_description=long_description,
    url='',
    author='phpusr',
    author_email='phpusr@gmail.com',
    install_requires=[
        'celery >=5.0.5, <5.6',
        'redis >=3.5.3, <6.2',
    ],
    extras_require={
        'gdrive': ['google-api-python-client >=2.2.0, <2.3.0'],
        'yandex-disk': ['requests >=2.32, <2.33']
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9'
    ]
)
