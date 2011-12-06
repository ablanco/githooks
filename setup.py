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
from setuptools import setup

from githooks import version


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="githooks",
    version=version,
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
