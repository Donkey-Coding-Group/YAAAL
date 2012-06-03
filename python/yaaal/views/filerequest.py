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
import scss
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

def scssfile(filename):
    """ *Public*. Returns a compiled Scss file. """
    with open(filename) as fl:
        return scss.Scss().compile(fl.read())

def res_request(request):
    """ *View*. Sends the requested file from the `res` folderto the
        client. """

    return file_request(request, os.path.join(maindir, 'res'), True)

    """
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

    data = None
    mime = None
    if suffix in 'css js html htm svg'.split():
        mime = 'text/%s' % suffix
    elif suffix in 'txt '.split():
        mime = 'text/plain'
    elif suffix in 'jpg jpeg png tif tiff gif':
        mime = 'image/%s' % suffix
    elif suffix in 'py pyw'.split():
        return cgifile(filename, request)
    elif suffix in 'scss '.split():
        data = scssfile(filename)
        mime = 'text/css'
    else:
        mime = 'file/%s' % suffix

    if mime:
        request.headers['Content-type'] = mime

    if not data:
        with open(filename) as fl:
            return fl.read()

    return data
    """

def file_request(request, rel_path=None, cgi=False):
    """ *view*. Sends any requested file to the client. """

    filename = request.match.group(1)
    if rel_path:
        filename = os.path.join(rel_path, filename)
    elif not os.path.isabs(filename):
        request.invoke_404()
        return

    if not os.path.exists(filename) or not os.path.isfile(filename):
        request.invoke_404()
        return

    suffix = filename.rfind('.')
    if suffix >= 0:
        suffix = filename[suffix + 1:]
    else:
        suffix = None

    data = None
    mime = None
    if suffix in 'css js html htm'.split():
        mime = 'text/%s' % suffix
    elif suffix in 'txt '.split():
        mime = 'text/plain'
    elif suffix in 'jpg jpeg png tif tiff gif':
        mime = 'image/%s' % suffix
    elif suffix in 'svg '.split():
        mime = 'image/%s+xml' % suffix
    elif suffix in 'py pyw'.split():
        if cgi:
            return cgifile(filename, request)
        else:
            with open(filename) as fl:
                data = fl.read()
            mime = 'text/plain'
    elif suffix in 'scss '.split():
        if cgi:
            data = scssfile(filename)
            mime = 'text/css'
        else:
            with open(filename) as fl:
                data = fl.read()
            mime = 'file/scss'
    else:
        mime = 'file/%s' % suffix

    if mime:
        request.headers['Content-type'] = mime

    if not data:
        with open(filename) as fl:
            data = fl.read()

    return data


