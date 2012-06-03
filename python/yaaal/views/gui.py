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

from __main__ import __file__ as mainfile
maindir = os.path.dirname(mainfile)

import yaaal.util.jinja2   as jutils
import models.applications as apps


def applist(request):
    template = os.path.join(maindir, 'templates', 'applist.jtmp')
    apps_ = apps.get_registered_applications().values()
    return jutils.render_template(template, {'apps':apps_, 'addable':False})


def appfind(request):
    template = os.path.join(maindir, 'templates', 'applist.jtmp')
    apps_ = apps.get_found_apps().values()
    return jutils.render_template(template, {'apps':apps_, 'addable':True})




