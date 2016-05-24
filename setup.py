# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pyantidot

setup(
    name='python-antidot',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'nose',
        'requests',
        'Werkzeug',
    ],
    author='Algoo',
    author_email="contact@algoo.fr",
    description='Python antidot search engine implementation, see '
                'https://github.com/algoo/python-antidot.',
    long_description='Python antidot search engine implementation, see '
                'https://github.com/algoo/python-antidot.',
    include_package_data=True,
    url='https://github.com/algoo/python-antidot',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU Affero General Public "
        "License v3 or later (AGPLv3+)"
    ]
)
