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
import os.path
import sys
import re
import shutil
import tempfile
import subprocess

version = "0.1.1dev"

re_options = re.IGNORECASE | re.MULTILINE | re.DOTALL
skip_pattern = re.compile('# githooks: (.*)', re_options)


class MercurialUI(object):

    def debug(self, text):
        # TODO print only in debug mode
        print text

    def warn(self, text):
        sys.stderr.write(text + "\n")

    def config(self, arg1, arg2, arg3=None):
        # TODO access config
        return ''


class MercurialChange(object):

    def __init__(self, revision):
        self.revision = revision
        self.gitcmd = GitCommands()

    def rev(self):
        # Return revision number (none in git)
        return ''

    def hex(self):
        # Return the hexadecimal code of the change
        return self.revision

    def description(self):
        return self.gitcmd.getDescription(self.rev)

    def user(self):
        return self.gitcmd.getAuthor(self.rev)

    def date(self):
        date = self.gitcmd.getDate(self.rev)
        # TODO convert date into hg format
        return date


class GitCommands(object):

    def _exec(self, proc):
        p = subprocess.Popen(proc, stdout=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def getDescription(self, revision):
        desc = self._exec(['git', 'cat-file', '-p', revision]).splitlines()
        desc = desc[5:]
        return "\n".join(desc)

    def getAuthor(self, revision):
        # TODO
        return ""

    def getDate(self, revision):
        # TODO
        return ""

    def getFileNames(self, old_revision, revision):
        files = self._exec(['git', 'log', '--name-only', "--pretty=format:''",
                            old_revision + '..' + revision])
        files = set(files.splitlines())
        result = []
        for f in files:
            if f != '' and f != "''":
                result.append(f)
        return result

    def getFileData(self, revision, filename):
        tree = self._exec(['git', 'cat-file', '-p', revision])
        tree = tree.splitlines()[0].split(" ")[1]
        return self._exec(['git', 'show', tree + ':' + filename])


class CheckerManager(object):

    def __init__(self, ui, revisions, initial_revision, skip_text=None):
        self.ui = ui
        self.revisions = revisions
        self.initial_revision = initial_revision
        self.skip_text = skip_text
        self.gitcmd = GitCommands()

    def skip_file(self, filename, filedata):
        if not filename.endswith('.py'):
            return True

        for match in skip_pattern.findall(filedata):
            if self.skip_text in match:
                return True

        return False

    def check(self, checker):
        warnings = 0
        old_rev = self.initial_revision
        for current_rev in self.revisions:
            rev_warnings = 0
            directory = tempfile.mkdtemp(suffix='-r' + current_rev,
                                         prefix='githooks')

            self.ui.debug(checker.__name__ + " -> Checking revision "
                          + current_rev)

            description = self.gitcmd.getDescription(current_rev)
            if self.skip_text and self.skip_text in description:
                continue

            files_to_check = {}
            revision_files = self.gitcmd.getFileNames(old_rev, current_rev)

            for filename in revision_files:
                if not(filename and filename != ""):
                    continue

                # TODO check if the file was removed in this changeset

                filedata = self.gitcmd.getFileData(current_rev, filename)

                if self.skip_text and self.skip_file(filename, filedata):
                    continue

                full_path = os.path.join(directory, filename)
                os.makedirs(os.path.split(full_path)[0])
                f = open(full_path, 'w')
                f.write(filedata)
                f.close()
                files_to_check[full_path] = filedata

            if files_to_check:
                rev_warnings += checker(files_to_check, description)

            if rev_warnings:
                self.ui.warn((checker.__name__
                              + ' -> %d warnings found in revision ' +
                              current_rev + '\n') % rev_warnings)
            else:
                self.ui.debug(checker.__name__ + ' -> No warnings in revision '
                              + current_rev + ' - Good job!\n')
            warnings += rev_warnings
            shutil.rmtree(directory)
            old_rev = current_rev

        if warnings:
            return True   # failure
        else:
            return False  # sucess
