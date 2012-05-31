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

import yaaal.util.jinja2    as jutil

from __main__ import __file__ as mainfile
maindir = os.path.dirname(mainfile)

templates = os.path.join(maindir, 'res', 'templates')

def GET_symbols(request):
    """ *View*. Loads the 'GET-symbols' template. """

    GETsym_dir = os.path.join(templates, 'GET-symbols')

    options = request.GET.get('options')
    if not options:
        filename = 'error.jtp'
        context = {}
    else:
        filename = 'view.jtp'
        context = {'options': options[0].split('|')}

    return jutil.render_template(os.path.join(GETsym_dir, filename), context)



