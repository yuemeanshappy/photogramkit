#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup

# build command
setup(
	name="photogramkit",
	version="0.0.1",
	author="Yue Yang",
	author_email="yy3098@columbia.edu",
	license="GPLv3",
	description="A package for automating photo sorting and 3D model building",
	classifiers=["Programming Language :: Python :: 3"],
	entry_points={
		"console_scripts": [
			"photogramkit = photogramkit.__main__:main"
		]
	}
	)