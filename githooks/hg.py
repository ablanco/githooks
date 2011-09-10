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

from githooks.git import git_author, git_date, git_description, git_config
from githooks.git import GLOBAL_CONTEXT


class MercurialUI(object):

    def debug(self, text):
        # TODO print only in debug mode
        print text

    def warn(self, text):
        sys.stderr.write(text + "\n")

    def config(self, family, variable, default=None, context=GLOBAL_CONTEXT):
        value = git_config('githooks', '%s.%s' % (family, variable), context)
        if value == '' and default is not None:
            return default
        else:
            return value


class MercurialChange(object):

    def __init__(self, revision):
        self.revision = revision

    def rev(self):
        # Return revision number (none in git)
        return ''

    def hex(self):
        # Return the hexadecimal code of the change
        return self.revision

    def description(self):
        return git_description(self.rev)

    def user(self):
        return git_author(self.rev)

    def date(self):
        date = git_date(self.rev)
        # TODO convert date into hg format
        return date
