#!/usr/bin/env python

from os.path import join, dirname, abspath

from setuptools import setup, find_packages


__AUTHOR__ = 'Bogdan Virtosu'
__AUTHOR_EMAIL__ = 'virtosu.bogdan@gmail.com'
__README_PATH__ = join(abspath(dirname(__file__)), 'README.md')
__README__ = open(__README_PATH__).read()

setup(
    name='cmsplugin-profile',
    version='0.0.1',
    description='CMS Plugin for profiles',
    long_description=__README__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    maintainer_email=__AUTHOR_EMAIL__,
    url='https://github.com/virtosubogdan/cmsplugin-profile.git',
    packages=find_packages(),
    include_package_data=True,
    platforms=['any'],
    install_requires=[
        'django-cms>=2.3,<2.3.6',
    ],
)
