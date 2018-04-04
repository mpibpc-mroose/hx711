#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('ReadMe.md') as readme_file:
    readme = readme_file.read()

setup(
    name='hx711',
    version='1.1.2',
    description="A library to drive a HX711 load cell amplifier on a Raspberry Pi",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Marco Roose",
    author_email='marco.roose@gmx.de',
    url='https://github.com/mpibpc-mroose/hx711',
    packages=find_packages(include=['hx711']),
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='hx711',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)
