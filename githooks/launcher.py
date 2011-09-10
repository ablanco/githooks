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

from githooks import CheckerManager
from githooks.hg import MercurialUI, MercurialChange
from githooks.git import REPOSITORY_CONTEXT


def main():

    result = False

    try:
        ui = MercurialUI()

        # Parameters
        # 0 to next to last: git revisions to check
        # last: initial revision

        revs = sys.argv[1:-1]
        ini_rev = sys.argv[-1:]
        ini_rev = ini_rev[0]
        revs.reverse()

        # PEP8, PDB and PYFLAKES

        # Pep8, pdb and pyflakes checkers

        pep8CM = CheckerManager(ui, revs, ini_rev, 'no-pep8')
        pdbCM = CheckerManager(ui, revs, ini_rev, 'no-pdb')
        pyflakesCM = CheckerManager(ui, revs, ini_rev, 'no-pyflakes')

        pep8_ignores = ui.config('pep8', 'ignore', '')

        # Check pep8, pdb and pyflakes

        result = pep8CM.check(pep8_checker(pep8_ignores))
        result = pdbCM.check(pdb_checker) or result
        result = pyflakesCM.check(pyflakes_checker) or result

        # TRAC

        track_hook_active = ui.config('trac', 'hook_active', False, REPOSITORY_CONTEXT)

        if track_hook_active:
            from hghooks.trachooks import TicketChecker, TicketUpdater
            from hghooks.trachooks import load_ticket_commands

            trac_env = ui.config('trac', 'environment', context=REPOSITORY_CONTEXT)

            #if trac_env is None:
            #ui.warn('You must set the environment option in the [trac] section'
                    #' of the repo configuration to use this hook')
            #return True  # failure

            # Trac ticket mention checker

            tracCM = CheckerManager(ui, revs, ini_rev, 'no-pyflakes')

            ticket_commands = load_ticket_commands()
            ticket_words = ticket_commands.keys()

            # Check trac ticket mention

            result = tracCM.check(TicketChecker(trac_env, ticket_words, ui)) or result

            # Trac ticket comments updater

            repo_name = ui.config('trac', 'repo_name', context=REPOSITORY_CONTEXT)
            changeset_style = ui.config('trac', 'changeset_style', 'short-hex',
                                        REPOSITORY_CONTEXT)
            msg_template = ui.config('trac', 'msg_template',
                                     '(At [%(changeset)s]) %(msg)s',
                                     REPOSITORY_CONTEXT)
            msg_template = unicode(msg_template, 'utf-8')

            ticket_updater = TicketUpdater(trac_env, repo_name, changeset_style,
                                        msg_template, ui)

            # Update trac ticket comments

            for rev in revs:
                ticket_updater(MercurialChange(rev))

        # Return result value

        if result:
            sys.exit(1)  # failure
        else:
            sys.exit(0)  # success

    except:
        sys.exit(1)  # when error always default to failure

if __name__ == '__main__':
    main()
