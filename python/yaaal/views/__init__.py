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

from __main__ import __file__

import os
import logging

__path__ = os.path.dirname(__file__)

def request_file(request):
    """ *View*. Sends a file to the client. The match-object must contain
        the file-name in it's second group. """

    filename = request.match.group(1)
    filename = os.path.join(__path__, 'res', filename)

    if not os.path.exists(filename) or not os.path.isfile(filename):
        request.invoke_404()
        return

    suffix = filename.rfind('.')
    if suffix >= 0:
        suffix = filename[suffix + 1:]
    else:
        suffix = None

    mime = None
    if suffix in 'css js html htm svg'.split():
        mime = 'text/%s' % suffix
    elif suffix in 'txt '.split():
        mime = 'text/plain'
    elif suffix in 'jpg jpeg png tif tiff gif':
        mime = 'image/%s' % suffix
    else:
        mime = 'file/%s' % suffix

    if mime:
        request.headers['Content-type'] = mime

    with open(filename) as fl:
        return fl.read()

def index(request):
    return "<html><body><h1>Welcome!</h1></body></html>"

def error(*args):
    raise Exception




