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

import sys

from hghooks.code import pep8_checker, pdb_checker, pyflakes_checker
from githooks import CheckerManager, MercurialUI


def main():

    ui = MercurialUI()

    revs = sys.argv[1:-1]
    ini_rev = sys.argv[-1:]
    ini_rev = ini_rev[0]
    revs.reverse()

    pep8CM = CheckerManager(ui, revs, ini_rev, 'no-pep8')
    pdbCM = CheckerManager(ui, revs, ini_rev, 'no-pdb')
    pyflakesCM = CheckerManager(ui, revs, ini_rev, 'no-pyflakes')

    result = False

    result = result or pep8CM.check(pep8_checker)
    result = result or pdbCM.check(pdb_checker)
    result = result or pyflakesCM.check(pyflakes_checker)

    if result:
        sys.exit(1)  # failure
    else:
        sys.exit(0)  # success

if __name__ == '__main__':
    main()
