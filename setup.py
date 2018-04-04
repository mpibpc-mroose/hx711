#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

__requires__ = ['pipenv']

packages = find_packages(exclude=['tests'])
base_dir = pathlib.Path(__file__).parent

pipenv_command = ['pipenv', 'install', '--deploy', '--system']
pipenv_command_dev = ['pipenv', 'install', '--dev', '--deploy', '--system']


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        subprocess.check_call(pipenv_command_dev)
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        subprocess.check_call(pipenv_command)
        install.run(self)


with open(str(base_dir / 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='hx711',
    version='1.1.2',
    description="A library to drive a HX711 load cell amplifier on a Raspberry Pi",
    url='https://github.com/mpibpc-mroose/hx711/',
    author="Marco Roose",
    author_email='marco.roose@gmx.de',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/mpibpc-mroose/hx711/issues',
    },
    use_scm_version=True,
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=packages,
    package_data={},
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='hx711',
    setup_requires=['setuptools_scm'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    test_suite='tests',
)

