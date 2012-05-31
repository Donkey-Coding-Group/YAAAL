# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys

import glob
import json
import ConfigParser

def parse_desktop_file(filename):
    """ *Public*. Parse a ``*.desktop`` file and return a dictionary of
        information. Raise ``OSError`` if *filename* does not exist.
        Raises ``ValueError`` the file is not valid. """

    if not os.path.exists(filename) or not os.path.isfile(filename):
        raise OSError('filename does not exist or is not a file.')

    parser = ConfigParser.ConfigParser()
    parser.read([filename])

    if not parser.has_section('Desktop Entry'):
        raise ValueError('the file does not contain a `Desktop Entry` section.')

    return dict(parser.items('Desktop Entry'))

def parse_for_desktop_files(path):
    """ *Public*. Parse ``*.desktop`` files located in the directory *path*.
        Raise ``OSError`` if *path* does not exist or is not a directory. """

    if not os.path.exists(path) or not os.path.isdir(path):
        raise OSError('path does not exist or is not a directory.')

    apps = []

    for filename in glob.glob(os.path.join(path, '*.desktop')):
        if not os.path.isfile(filename):
            continue

        fullname = os.path.join(path, filename)

        try:
            apps.append(parse_desktop_file(fullname))
        except ValueError:
            pass

    return apps


