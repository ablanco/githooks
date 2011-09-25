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

import datetime
import subprocess

GLOBAL_CONTEXT = 'global'
REPOSITORY_CONTEXT = 'local'
SYSTEM_CONTEXT = 'system'

__MONTHS = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Ago': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dic': 12,
}


def __execute_command(proc):
    p = subprocess.Popen(proc, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def __gittime2datetime(git_date):
    git_date = git_date.split(' ')
    day = int(git_date[2])
    month = __MONTHS[git_date[1]]
    year = int(git_date[4])
    time = git_date[3].split(':')
    #time_zone = TODO
    return datetime.datetime(year, month, day, int(time[0]), int(time[1]),
                             int(time[2]))


def config(family, variable, context):
    value = __execute_command(['git', 'config', '--%s' % context,
                              '%s.%s' % (family, variable)])
    return value[:-1]


def description(revision):
    desc = __execute_command(['git', 'cat-file', '-p', revision]).splitlines()
    desc = desc[5:]
    return "\n".join(desc)


def author(revision):
    log = __execute_command(['git', 'log', revision, '-n', '1']).splitlines()
    return log[2][8:]


def date(revision):
    log = __execute_command(['git', 'log', revision, '-n', '1']).splitlines()
    date = log[3][8:]
    return __gittime2datetime(date)


def file_names(old_revision, revision):
    files = __execute_command(['git', 'log', '--name-only',
                              "--pretty=format:''",
                              old_revision + '..' + revision])
    files = set(files.splitlines())
    result = []
    for f in files:
        if f != '' and f != "''":
            result.append(f)
    return result


def file_data(revision, filename):
    tree = __execute_command(['git', 'cat-file', '-p', revision])
    tree = tree.splitlines()[0].split(" ")[1]
    return __execute_command(['git', 'show', tree + ':' + filename])
