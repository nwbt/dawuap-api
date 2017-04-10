#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: setup.py Project: webapi-2.7
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

from setuptools import setup, find_packages

setup(
    name="DawuapWebAPI",
    version="0.1",
    packages=find_packages(),

    install_requires=[
        'cherrypy',
        'uwsgi',
        'requests', 'geojson', 'pyproj'
    ],

    extras_require={
        'DEBUG': [
            'ipython',
            'ipdb',
            'pdb',
            'configparser',
        ],
    },

    author="Dan Catalano",
    author_email="dev@nwbt.co",
    description="",
    license="MIT",
    keywords="",
    url="",
)
