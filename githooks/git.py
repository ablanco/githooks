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

import subprocess


def execute_command(proc):
    p = subprocess.Popen(proc, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def git_description(revision):
    desc = execute_command(['git', 'cat-file', '-p', revision]).splitlines()
    desc = desc[5:]
    return "\n".join(desc)


def git_author(revision):
    # TODO
    return ""


def git_date(revision):
    # TODO
    return ""


def git_file_names(old_revision, revision):
    files = execute_command(['git', 'log', '--name-only', "--pretty=format:''",
                            old_revision + '..' + revision])
    files = set(files.splitlines())
    result = []
    for f in files:
        if f != '' and f != "''":
            result.append(f)
    return result


def git_file_data(revision, filename):
    tree = execute_command(['git', 'cat-file', '-p', revision])
    tree = tree.splitlines()[0].split(" ")[1]
    return execute_command(['git', 'show', tree + ':' + filename])
