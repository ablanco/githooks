# Copyright (C) 2011  Alejandro Blanco Escudero <alejandro.b.e@gmail.com>
#
# This file is part of githooks
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import codecs
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))


# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(HERE, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read(*rnames):
    return open(os.path.join(HERE, *rnames)).read()


setup(
    name="githooks",
    version=find_version("githooks", "__init__.py"),
    author="Alejandro Blanco Escudero",
    author_email="alejandro.b.e@gmail.com",
    description=("Set of Git hooks for pep8, pyflakes, jslint and trac "
                 "integration"),
    long_description=read('README.rst'),
    license="GPL 3",
    keywords="git hook pep8 pyflakes jslint trac",
    packages=['githooks'],
    url='https://github.com/ablanco/githooks/',
    zip_safe=False,
    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Intended Audience :: System Administrators",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Natural Language :: English",
                 "Programming Language :: Python",
                 "Programming Language :: JavaScript",
                 "Topic :: Software Development :: Version Control",
                 "Topic :: Software Development :: Quality Assurance"],
    install_requires=[
        'setuptools',
        'pep8',
        'pyflakes',
        'pyjslint',
        'hghooks',
        ],
    entry_points={
        'console_scripts': [
            'githooks = githooks.launcher:main',
            ]},
)
