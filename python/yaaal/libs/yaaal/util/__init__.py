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

import sys
import logging

_initialized_logger = False

class MultilineFormatter(logging.Formatter):
    """ *Public*. A formatter to handle multiline log-messages.
        Thanks to http://mail.python.org/pipermail/python-list/2010-November/1259582.html.
        """

    def format(self, record):
        str = logging.Formatter.format(self, record)
        if not record.message:
            return str

        header, footer = str.split(record.message)
        str = str.replace('\n', '\n%s' % (' ' * len(header)))
        return str

def stderr_logger():
    """ *Public*. Builds and return a logger to stdout with name
        ``yaaal-stderr``. """
    global _initialized_logger

    logger = logging.getLogger('yaaal-stderr')
    if not _initialized_logger:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = MultilineFormatter('%(asctime)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        _initialized_logger = True

    return logger


