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
import jinja2
import cStringIO

from __main__ import __file__ as mainfile
maindir = os.path.dirname(mainfile)

def cgifile(filename, request):
    """ *Public*. Executes a cgi Python-file in an environment where *request*
        is available under the same name. """

    code = None
    with open(filename) as fl:
        code = fl.read()

    code = compile(code, filename, 'exec')

    stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()

    globals = dict(request = request, __file__ = filename,
                   __name__ = '__main__')
    exec code in globals

    sys.stdout.seek(0)
    try:
        return sys.stdout.read()
    finally:
        sys.stdout = stdout

def file_request(request):
    """ *View*. Sends the requested file to the client. """

    filename = request.match.group(1)
    filename = os.path.join(maindir, 'res', filename)

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
    elif suffix in 'py pyw'.split():
        return cgifile(filename, request)
    else:
        mime = 'file/%s' % suffix

    if mime:
        request.headers['Content-type'] = mime

    with open(filename) as fl:
        return fl.read()


