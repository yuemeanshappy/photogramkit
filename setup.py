#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup, find_packages

# build command
setup(
	name="photogramkit",
	version="0.0.1",
	author="Yue Yang",
	author_email="yy3098@columbia.edu",
	license="GPLv3",
	description="A package for automating photo sorting and 3D model building",
	classifiers=["Programming Language :: Python :: 3"],
	packages=find_packages(include=["photogramkit", "photogramkit.*"]), # only install the photogramkit package rather than the notebook package
	entry_points={
		"console_scripts": [
			"photogramkit = photogramkit.__main__:main"
		]
	},
	install_requires=[
        'pyexiftool==0.4.13'
    ]
	)